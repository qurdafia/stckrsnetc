# Generated by Django 3.0.7 on 2021-04-01 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0002_auto_20210330_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='ordermodel',
            name='city',
            field=models.CharField(default='', max_length=200),
        ),
        migrations.AddField(
            model_name='ordermodel',
            name='zip_code',
            field=models.CharField(default='', max_length=4),
        ),
    ]