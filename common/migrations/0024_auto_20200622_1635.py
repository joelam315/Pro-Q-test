# Generated by Django 2.2.4 on 2020-06-22 08:35

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0023_auto_20200622_1555'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, unique=True),
        ),
    ]
