from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from datetime import datetime

from phone_field import PhoneField
from django.core.exceptions import ValidationError
# Create your models here.


class UserRegistrationModel(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)


MATERIALS = [("sticker", "STICKER"),]
COUNTRIES = [("PH", "Philippines"),]

def validate_image(image):
    file_size = image.file.size
    limit_kb = 2621440
    if file_size > limit_kb:
        raise ValidationError("Max size of file is %s KB" % limit_kb)


class OrderModel(models.Model):
    material = models.CharField(max_length=200, choices=MATERIALS, default="sticker")
    customer = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    location = models.CharField(max_length=200,choices=COUNTRIES, default="PH")
    address = models.CharField(max_length=500, blank=False)
    mobile = models.CharField(max_length=50, blank=True)
    width = models.PositiveIntegerField(blank=False, default=0)
    height = models.PositiveIntegerField(blank=False, default=0)
    quantiy = models.PositiveIntegerField(blank=False, default=0)
    order_date = models.DateTimeField(default=datetime.now, blank=True)
    file = models.ImageField("Image", upload_to="documents/%Y/%m/%d/", validators=[validate_image], default="", blank=True)
    total_price = models.DecimalField(default=0.0, blank=True, null=True, max_digits=20, decimal_places=10)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return str(self.id)
        #return str(self.order_date)
