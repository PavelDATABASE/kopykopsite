from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    phone = models.CharField(max_length=15, verbose_name="Телефон", blank=True, null=True)
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', verbose_name="Аватарка", null=True, blank=True)
    
    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"
    
    def __str__(self):
        return f"Профиль {self.user.username}"


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    """Создаёт профиль при создании пользователя"""
    if created:
        Profile.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    """Сохраняет профиль при изменении пользователя"""
    instance.profile.save()

class PriceList(models.Model):
    name = models.CharField(max_length=100, verbose_name="Наименование услуги", null=True, blank=True)
    count = models.CharField(max_length=10, verbose_name="Стоимость", null=True, blank=True)
    

    class Meta:
        ordering = ('id', )
        verbose_name = 'Услуга'
        verbose_name_plural = 'Услуги'
        
    def __str__(self):
        return self.name
    
    
class News(models.Model):
    images = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name="Изображение", null=True, blank=True)
    images_title_big = models.CharField(max_length=100, verbose_name="Текст услуги (большой)", null=True, blank=True)
    images_title = models.CharField(max_length=100, verbose_name="Текст услуги (средний)", null=True, blank=True)
    images_description = models.CharField(max_length=100, verbose_name="Описание услуги", null=True, blank=True)
    
    class Meta:
        ordering = ('id', )
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        
    def __str__(self):
        return self.images_title_big or self.images_title or "Без названия"
    
    
def order_file_path(instance, filename):
    """Генерирует уникальный путь для файла заказа"""
    import uuid
    import os
    ext = filename.split('.')[-1]
    new_filename = f'order_{uuid.uuid4().hex}.{ext}'
    return f'orders/{new_filename}'


class Orders(models.Model):
    name = models.ForeignKey(PriceList, on_delete=models.CASCADE, related_name='names')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders', null=True, blank=True)
    
    orders_name = models.CharField(max_length=100, verbose_name="Название заказа", null=True, blank=True)
    number = models.CharField(max_length=15, verbose_name="Номер телефона", null=True, blank=True)
    fio = models.CharField(max_length=100, verbose_name="Ф.И", blank=True, null=True)
    description = models.CharField(max_length=200, verbose_name="Дополнительная информация", null=True, blank=True)
    file = models.FileField(upload_to=order_file_path, verbose_name="Файл", max_length=255, null=True, blank=True)
    
    class Meta:
        ordering = ('id', )
        verbose_name = "Заказ"
        verbose_name_plural = "Заказы"
        
    def save(self, *args, **kwargs):
        # Если orders_name не установлен, генерируем автоматически
        if not self.orders_name:
            # Сначала сохраняем объект, чтобы получить ID
            super().save(*args, **kwargs)
            # Теперь у нас есть ID, генерируем название
            self.orders_name = f"Заказ #{self.id}"
            # Сохраняем снова с обновлённым названием
            super().save(update_fields=['orders_name'])
        else:
            super().save(*args, **kwargs)
        
    def __str__(self):
        return self.orders_name or "Без названия"
        