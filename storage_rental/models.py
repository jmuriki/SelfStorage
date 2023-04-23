import qrcode
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission, Group


def create_qr_code():
    data = 'Мама мыла раму, сидя на подоконнике'  # self.get_order_num(self.id, self.user)
    filename = f'{data}.png'
    qrcode.make(data).save(filename)
    return filename


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    email = email = models.EmailField(max_length=320, blank=True)
    name = models.CharField(max_length=250, blank=True)
    surname = models.CharField(max_length=250, blank=True)
    phone_number = PhoneNumberField(blank=True)
    bookings = models.ManyToManyField('Order', related_name='customers', blank=True)

    groups = models.ManyToManyField(
        'auth.Group',
        verbose_name='groups',
        blank=True,
        related_name='storage_rental_users'
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        verbose_name='user permissions',
        blank=True,
        related_name='storage_rental_users_permissions'
    )

    def __str__(self):
        return self.email


class Cell(models.Model):
    cell_id = models.IntegerField(primary_key=True)
    capacity = models.FloatField()
    occupied = models.BooleanField(default=False)
    occupied_until = models.DateTimeField()
    price = models.CharField(max_length=250)

    class Meta:
        verbose_name_plural = "Ячейки"


class Storage(models.Model):
    storage_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    city = models.CharField(max_length=250)
    address = models.CharField(max_length=1024)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    count_cells = models.IntegerField()
    count_free_cells = models.IntegerField()
    temperature = models.FloatField()
    height = models.FloatField()
    cells = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='storage_cells')

    class Meta:
        verbose_name_plural = "Склады"


class Image(models.Model):
    image = models.ImageField(upload_to='image')
    image_number = models.IntegerField(default=0, blank=True)
    storage = models.ForeignKey(Storage, on_delete=models.CASCADE, related_name='imgs')

    class Meta:
        ordering = ['image_number']
        verbose_name_plural = "Картинки"


class Order(models.Model):
    user_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    start_booking = models.DateTimeField()
    end_booking = models.DateTimeField()
    status = models.CharField(max_length=250, default='создан')

    class Meta:
        unique_together = ['cell_id']
        verbose_name_plural = "Заказы"


class Alert(models.Model):
    user = models.ManyToManyField('Customer')
    alert_name = models.CharField(max_length=250)
    alert_text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, default='отправлено')

    class Meta:
        verbose_name_plural = "Оповщения"
