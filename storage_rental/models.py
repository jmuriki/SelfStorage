from django.db import models
import qrcode

# Create your models here.


def create_qr_code():
    data = 'Мама мыла раму, сидя на подоконнике'  # self.get_order_num(self.id, self.user)
    filename = f'{data}.png'
    qrcode.make(data).save(filename)
    return filename
