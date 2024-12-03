# Generated by Django 2.2.4 on 2020-06-22 07:55

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0022_auto_20200622_1554'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, unique=True),
            preserve_default=False,
        ),
    ]