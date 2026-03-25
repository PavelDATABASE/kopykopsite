from django.contrib import admin
from .models import PriceList, News, Orders, Profile

admin.site.register(PriceList)
admin.site.register(News)
admin.site.register(Orders)
admin.site.register(Profile)