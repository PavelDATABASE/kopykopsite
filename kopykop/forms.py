from django import forms
from django.contrib.auth.models import User
from .models import Profile


class ProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    
    # Поля из модели User
    first_name = forms.CharField(label='Имя', max_length=30, required=False)
    last_name = forms.CharField(label='Фамилия', max_length=30, required=False)
    email = forms.EmailField(label='Email', required=False)
    
    class Meta:
        model = Profile
        fields = ['phone', 'avatar']
        labels = {
            'phone': 'Телефон',
            'avatar': 'Аватарка',
        }
        widgets = {
            'phone': forms.TextInput(attrs={
                'placeholder': 'Введите номер телефона',
                'class': 'form-input'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'avatar-input',
                'accept': 'image/*'
            }),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Заполняем поля данными из связанного User
        if self.instance and self.instance.user:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email
    
    def save(self, commit=True):
        profile = super().save(commit=False)
        user = profile.user
        
        # Обновляем данные пользователя
        user.first_name = self.cleaned_data.get('first_name', '')
        user.last_name = self.cleaned_data.get('last_name', '')
        user.email = self.cleaned_data.get('email', '')
        user.save()
        
        if commit:
            profile.save()
        
        return profile
