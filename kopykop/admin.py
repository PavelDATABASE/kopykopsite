from django.contrib import admin
from .models import PriceList, News, Orders

admin.site.register(PriceList)
admin.site.register(News)
admin.site.register(Orders)