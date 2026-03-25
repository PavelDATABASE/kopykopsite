from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.db.models import Q
from .models import PriceList, News, Orders, Profile
from .forms import ProfileForm
from .telegram_bot import notify_admin


@csrf_exempt
def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        email = request.POST.get('email')
        if password == password_confirm:
            user = User.objects.create_user(username=username, email=email, password=password)
            login(request, user) # Автоматический вход после регистрации
            return redirect('login')
        else:
            return HttpResponse("Пароли не совпадают")      
    return render(request, 'register.html')


@csrf_exempt
def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username = username, password = password)
        if user is not None: 
            login(request, user)
            return redirect('/')
        else: 
            return HttpResponse('Неправильный логин или пароль')
    return render(request, 'login.html')
        
def logout_view(request):
    logout(request)
    return redirect('login')
    
        
def price(request):
    price = PriceList.objects.all()
    return render(request, 'price.html', {'price':price})


def about(request):
    news = News.objects.all()
    return render(request, 'about.html', {'news':news})

def index(request):
    news = News.objects.all()
    return render(request, 'index.html', {'news': news})


@csrf_exempt
def orders(request):
    object = PriceList.objects.all()
    if request.method == 'POST':
        number = request.POST.get('number')
        fio = request.POST.get('fio')
        name_id = request.POST.get('name')
        description = request.POST.get('description')
        file = request.FILES.get('file')  # Получаем загруженный файл
        
        # Проверяем, что name_id получен и преобразуем в int
        if name_id:
            try:
                # Получаем объект PriceList по ID
                price_item = PriceList.objects.get(id=int(name_id))
                # Создаём профиль, если его нет
                if request.user.is_authenticated:
                    profile, _ = Profile.objects.get_or_create(user=request.user)
                obj = Orders.objects.create(
                    name=price_item,
                    number=number,
                    fio=fio,
                    description = description,
                    file=file,
                    user=request.user if request.user.is_authenticated else None
                )
                notify_admin(obj)
            except (PriceList.DoesNotExist, ValueError) as e:
                print(f"Error: {e}")
                return HttpResponse(f"Ошибка: {e}")
        else:
            return HttpResponse("ОШИБКА! Выберите услугу")
    return render(request, 'orders.html', {'object': object})


def orders_list(request):
    query = request.GET.get('q', '')  # Получаем поисковый запрос из URL
    
    if query:
        # Ищем по всем полям модели Orders
        # Q позволяет использовать OR/AND условия
        object_list = Orders.objects.filter(
            Q(orders_name__icontains=query) |  # Название заказа
            Q(name__name__icontains=query) |    # Наименование услуги (через ForeignKey)
            Q(fio__icontains=query) |           # ФИО
            Q(number__icontains=query)          # Номер телефона
        )
    else:
        object_list = Orders.objects.all()
    
    return render(request, 'orders_list.html', {
        'obj': object_list,
        'query': query  # Передаём запрос обратно в шаблон
    })


def profile(request):
    if not request.user.is_authenticated:
        return redirect('login')
    
    # Создаём профиль, если его нет (для существующих пользователей)
    profile, created = Profile.objects.get_or_create(user=request.user)
    
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    
    # Получаем заказы текущего пользователя
    user_orders = Orders.objects.filter(user=request.user).order_by('-id')
    
    return render(request, 'profile.html', {
        'user_orders': user_orders,
        'form': form
    })