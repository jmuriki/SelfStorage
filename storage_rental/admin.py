from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name']
    fields = ['user', 'first_name', 'last_name', 'email', 'phone_number', 'avatar']


class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'description', 'temperature', 'height']
    fields = ['name', 'city', 'address', 'description', 'temperature', 'height']


class CellAdmin(admin.ModelAdmin):
    list_display = ['storage', 'cell_number', 'level', 'height', 'width', 'length', 'capacity', 'price']
    fields = ['storage', 'cell_number', 'level', 'height', 'width', 'length', 'capacity', 'price']


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Cell, CellAdmin)
# admin.site.register(Storage)
# admin.site.register(Order)
# admin.site.register(Alert)
