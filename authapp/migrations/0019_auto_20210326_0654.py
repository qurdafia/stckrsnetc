# Generated by Django 3.0.9 on 2021-03-26 06:54

from django.db import migrations
import phone_field.models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0018_auto_20210326_0647'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='mobile',
            field=phone_field.models.PhoneField(max_length=31),
        ),
    ]
