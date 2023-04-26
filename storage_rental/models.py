from django.db import models
from django.db.models import F, Count, Q, Min
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission, Group
import datetime


class Customer(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    email = models.EmailField(
        max_length=320,
        blank=True,
        verbose_name='Адрес электронной почты'
    )
    avatar = models.ImageField(
        upload_to='',
        blank=True,
        verbose_name='Аватарка'
    )
    first_name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Имя'
    )
    last_name = models.CharField(
        max_length=250,
        blank=True,
        verbose_name='Фамилия'
    )
    phone_number = PhoneNumberField(
        region='RU',
        db_index=True,
        blank=True,
        verbose_name='Телефон'
    )

    def __str__(self):
        return f'{self.first_name} {self.last_name}, {self.email}'

    class Meta:
        verbose_name = 'Арендатор'
        verbose_name_plural = 'Арендаторы'


class StorageManager(models.Manager):
    def with_cells_count(self):
        return self.annotate(cells_count=Count('cells'))
    
    def with_free_cells_count(self):
        return self.annotate(free_cells_count=Count('cells', filter=Q(cells__occupied=False)))

    def with_min_price(self):
        return self.annotate(min_price=Min('cells__price'))

    def with_all_cells_filters(self):
        return self.annotate(
            cells_count=Count('cells'),
            free_cells_count=Count('cells', filter=Q(cells__occupied=False)),
            min_price=Min('cells__price'),
        )


class Storage(models.Model):
    name = models.CharField(
        max_length=255,
        blank=False,
        unique=True,
        verbose_name='Наименование')
    address = models.CharField(
        max_length=1024,
        blank=False,
        unique=True,
        verbose_name='Адрес')
    city = models.CharField(
        max_length=255,
        blank=False,
        verbose_name='Город'
    )
    description = models.CharField(
        max_length=1024,
        blank=False,
        verbose_name='Описание')
    temperature = models.FloatField(
        null=False,
        verbose_name='Температура хранения, гр. Цельсия'
    )
    height = models.FloatField(
        null=False,
        verbose_name='Высота потолка, м.'
    )
    image = models.ImageField(
        upload_to='',
        blank=True,
        verbose_name='Картинка'
    )

    objects = StorageManager()

    def __str__(self):
        return f'Склад "{self.name}", {self.city}, {self.address}, {self.description[:20]}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class CellManager(models.Manager):
    def with_square(self):
        return self.annotate(sq=F('width') * F('length'))
    
    def with_volume(self):
        return self.annotate(vol=F('width') * F('length') * F('height'))


class Cell(models.Model):
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        default=None,
        related_name='cells',
        verbose_name='Склад'
    )
    cell_number = models.CharField(
        max_length=20,
        blank=False,
        verbose_name='Каталожный номер ячейки'
    )
    level = models.IntegerField(
        null=False,
        verbose_name='Этаж'
    )
    height = models.FloatField(
        null=False,
        verbose_name='Высота, м.'
    )
    width = models.FloatField(
        null=False,
        verbose_name='Ширина, м.'
    )
    length = models.FloatField(
        null=False,
        verbose_name='Длина, м.'
    )
    occupied = models.BooleanField(
        default=False,
        verbose_name='Занята'
    )
    price = models.FloatField(
        null=False,
        verbose_name='Стоимость хранения в ячейке'
    )

    objects = CellManager()

    def __str__(self):
        return f'{self.storage.name}, {self.level} эт. №{self.cell_number}'

    @property
    def square(self):
        width = 0 if self.width is None else self.width
        length = 0 if self.length is None else self.length
        return width * length
    square.fget.short_description = 'Площадь ячейки, м.кв.'

    @property
    def capacity(self):
        width = 0 if self.width is None else self.width
        length = 0 if self.length is None else self.length
        height = 0 if self.height is None else self.height
        return width * length * height
    capacity.fget.short_description = 'Объём ячейки, м.куб.'

    class Meta:
        verbose_name = 'Ячейка'
        verbose_name_plural = 'Ячейки'


ORDER_STATUSES = [
    ('created', 'Создан'),
    ('closed', 'Завершён'),
    ('payed', 'Оплачен'),
    ('overdue', 'Просрочен'),
]


class Order(models.Model):
    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Заказчик'
    )
    cells = models.ManyToManyField(
        Cell,
        related_name='orders',
        verbose_name='Ячейки заказа'
    )
    date_from = models.DateField('Дата начала хранения', auto_now_add=True)
    date_to = models.DateField('Дата окончания хранения', auto_now_add=True)
    status = models.CharField(
        max_length=10,
        choices=ORDER_STATUSES,
        default='created',
        verbose_name='Статус заказа'
    )

    def __str__(self):
        return f'{self.customer}, {self.date_from.strftime("%d.%m.%Y")}-{self.date_to.strftime("%d.%m.%Y")}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


# class Alert(models.Model):
#     user = models.ManyToManyField('Customer')
#     alert_name = models.CharField(max_length=250)
#     alert_text = models.TextField(blank=True)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=250, default='отправлено')

#     class Meta:
#         verbose_name_plural = "Оповщения"
