import qrcode
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import Permission, Group


def create_qr_code():
    data = 'Мама мыла раму, сидя на подоконнике'  # self.get_order_num(self.id, self.user)
    filename = f'{data}.png'
    qrcode.make(data).save(filename)
    return filename


class User(AbstractUser):
    userid = models.IntegerField(primary_key=True)
    login = models.CharField(max_length=32, blank=True, unique=True)
    email = models.EmailField(max_length=320, blank=True)
    name = models.CharField(max_length=250)
    surname = models.CharField(max_length=250)
    phone_number = PhoneNumberField()
    bookings = models.ManyToManyField('Order', related_name='users')

    groups = models.ManyToManyField(
        Group,
        verbose_name='groups',
        blank=True,
        related_name='storage_rental_users'
    )
    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name='user permissions',
        blank=True,
        related_name='storage_rental_users_permissions'
    )

    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = 'email', 'name', 'surname', 'phone_number'

    def str(self):
        return self.login


class Cell(models.Model):
    cell_id = models.IntegerField(primary_key=True)
    capacity = models.FloatField()
    occupied = models.BooleanField(default=False)
    occupied_until = models.DateTimeField()
    price = models.CharField(max_length=250)


class Storage(models.Model):
    storage_id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=250)
    address = models.CharField(max_length=1024)
    phone_number = PhoneNumberField(blank=True)
    email = models.EmailField(blank=True)
    count_cells = models.IntegerField()
    count_free_cells = models.IntegerField()
    cells = models.ForeignKey(Cell, on_delete=models.CASCADE, related_name='storage_cells')


class Order(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    cell_id = models.ForeignKey(Cell, on_delete=models.CASCADE)
    start_booking = models.DateTimeField()
    end_booking = models.DateTimeField()
    status = models.CharField(max_length=250, default='создан')

    class Meta:
        unique_together = ['cell_id']


class Alert(models.Model):
    user = models.ManyToManyField('User')
    alert_name = models.CharField(max_length=250)
    alert_text = models.TextField(blank=True)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=250, default='отправлено')
