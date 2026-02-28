from django.db import models

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
    title = models.CharField(max_length=100, verbose_name="Заголовок новости", null=True, blank=True)
    title_big = models.CharField(max_length=100, verbose_name="Важная новость", null=True, blank=True)
    description = models.CharField(max_length=1000, verbose_name="Описание новости", null=True, blank=True)
    images = models.ImageField(upload_to='uploads/%Y/%m/%d/', verbose_name="Изображение", null=True, blank=True)
    
    class Meta:
        ordering = ('id', )
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
        
    def __str__(self):
        return self.title_big or self.title or "Без названия"
    
    
    