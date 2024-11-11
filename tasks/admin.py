from django.contrib import admin
from .models import Task

from .models import *

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(Plants)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)
admin.site.register(FavoritePlant   )
# Register your models here.


class TaskAdmin(admin.ModelAdmin):
    readonly_fields =("created",)
    
admin.site.register(Task)
