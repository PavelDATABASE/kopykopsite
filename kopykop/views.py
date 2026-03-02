from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from .models import PriceList, News, Orders


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
    return render(request, 'about.html')

def index(request):
    news = News.objects.all()
    return render(request, 'index.html', {'news': news})


@csrf_exempt
def orders(request):
    object = PriceList.objects.all()
    if request.method == 'POST':
        number = request.POST.get('number')
        fio = request.POST.get('fio')
        obj = Orders.objects.create(number = number, fio = fio)
    return render(request, 'orders.html', {'object': object, 'obj':obj})