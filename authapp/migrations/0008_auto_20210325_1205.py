# Generated by Django 3.0.9 on 2021-03-25 12:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authapp', '0007_ordermodel_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ordermodel',
            name='file',
            field=models.FileField(blank=True, default='', upload_to='documents/%Y/%m/%d/'),
        ),
    ]