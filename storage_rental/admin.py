from django.utils.html import format_html
from django.contrib import admin
from .models import *


class CustomerAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'email', 'phone_number']
    search_fields = ['first_name', 'last_name']
    fieldsets = (
        (None, {
                    'fields': (('user', 'first_name', 'last_name', ),
                               ('email', 'phone_number', ),
                               ('avatar', 'get_image_preview', )
                               )
                }
         ),
    )

    readonly_fields = [
        'get_image_preview',
    ]

    def get_image_preview(self, obj):
        if not obj.avatar:
            return 'Выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.avatar.url)
    get_image_preview.short_description = 'Предпросмотр'


class StorageAdmin(admin.ModelAdmin):
    list_display = ['name', 'city', 'address', 'description', 'temperature', 'height']
    fieldsets = (
        (None, {
                    'fields': (('name', 'description', ),
                               ('city', 'address', ),
                               ('temperature', 'height', ),
                               ('image', 'get_image_preview', )
                               )
                }
         ),
    )
    readonly_fields = [
        'get_image_preview',
    ]

    def get_image_preview(self, obj):
        if not obj.image:
            return 'Выберите картинку'
        return format_html('<img src="{url}" style="max-height: 200px;"/>', url=obj.image.url)
    get_image_preview.short_description = 'Предпросмотр'


class CellAdmin(admin.ModelAdmin):
    list_display = ['storage', 'cell_number', 'level', 'height', 'width', 'length', 'square', 'capacity', 'price']
    fieldsets = (
        (None, {
                    'fields': (('storage', ),
                               ('occupied', 'cell_number', 'level', ),
                               ('height', 'width', 'length', ),
                               ('square', 'capacity', ),
                               ('price', ),
                               )
                }
         ),
    )
    readonly_fields = [
        'square', 'capacity',
    ]
    list_filter = ['storage', ]


class CellsInline(admin.TabularInline):
    model = Order.cells.through
    raw_id_fields = ('cell',)
    verbose_name = 'Ячейка'
    verbose_name_plural = 'Ячейки заказа'
    extra = 0


class OrderAdmin(admin.ModelAdmin):
    list_display = ['customer', 'status', 'date_from', 'date_to']
    fieldsets = (
        (None, {
                    'fields': (('customer', 'status', ),
                               ('date_from', 'date_to', ),
                               )
                }
         ),
    )
    inlines = [CellsInline]


admin.site.register(Customer, CustomerAdmin)
admin.site.register(Storage, StorageAdmin)
admin.site.register(Cell, CellAdmin)
admin.site.register(Order, OrderAdmin)
# admin.site.register(Alert)
