from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(MyUser)
admin.site.register(Categories)
admin.site.register(Product)
admin.site.register(SessionMaster)
admin.site.register(ShoppingCart)
admin.site.register(ShipTime)
admin.site.register(OrderMaster)