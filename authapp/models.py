from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime
from django_countries.fields import CountryField
from phone_field import PhoneField
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


MATERIALS = [('sticker', 'STICKER'),]


class OrderModel(models.Model):
    material = models.CharField(max_length=200, choices=MATERIALS, default='sticker')
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    country = CountryField(multiple=False, default='PH')
    address = models.CharField(max_length=500, blank=False)
    mobile = PhoneField(blank=False)
    width = models.IntegerField(blank=False, default=0)
    height = models.IntegerField(blank=False, default=0)
    quantiy = models.IntegerField(blank=False, default=0)
    order_date = models.DateTimeField(default=datetime.now, blank=True)
    file = models.FileField(upload_to='documents/%Y/%m/%d/', default='', blank=True)
    total_price = models.DecimalField(default=0.00, max_digits=100, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
        #return str(self.order_date)
