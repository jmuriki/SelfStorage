from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission, Group


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

    def __str__(self):
        return f'Склад "{self.name}", {self.city}, {self.address}, {self.description[:20]}'

    class Meta:
        verbose_name = 'Склад'
        verbose_name_plural = 'Склады'


class Cell(models.Model):
    storage = models.ForeignKey(
        Storage,
        on_delete=models.CASCADE,
        default=None,
        related_name='storage',
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
    capacity = models.FloatField(
        null=False,
        verbose_name='Объём, м.куб.'
    )
    occupied = models.BooleanField(
        default=False,
        verbose_name='Занята'
    )
    price = models.FloatField(
        null=False,
        verbose_name='Стоимость хранения в ячейке'
    )

    def __str__(self):
        return f'{self.storage.name}, {self.level} эт. №{self.cell_number}'

    class Meta:
        verbose_name = 'Ячейка'
        verbose_name_plural = 'Ячейки'


# class Order(models.Model):
#     customer = models.ForeignKey(
#         Customer,
#         on_delete=models.CASCADE,
#         related_name='customer',
#         verbose_name='Заказчик'
#     )
#     cell = models.ManyToManyField(
#         Cell,
#         on_delete=models.CASCADE,
#         related_name='cells',
#         verbose_name='Ячейки'
#     )
#     date_from = models.DateTimeField('Дата начала хранения')
#     date_to = models.DateTimeField('Дата окончания хранения')
#     # Создан, Оплачен, Закрыт, Просрочен
#     status = models.CharField(
#         max_length=250,
#         default='создан'
#     )
#
#     class Meta:
#         verbose_name = 'Заказ'
#         verbose_name_plural = 'Заказы'


# class Image(models.Model):
#     image = models.ImageField(upload_to='')
#     image_number = models.IntegerField(default=0, blank=True)
#     storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='imgs')

#     class Meta:
#         ordering = ['image_number']
#         verbose_name_plural = "Картинки"


# class Alert(models.Model):
#     user = models.ManyToManyField('Customer')
#     alert_name = models.CharField(max_length=250)
#     alert_text = models.TextField(blank=True)
#     date = models.DateTimeField(auto_now_add=True)
#     status = models.CharField(max_length=250, default='отправлено')

#     class Meta:
#         verbose_name_plural = "Оповщения"
