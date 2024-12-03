# Generated by Django 2.2.4 on 2021-02-10 04:36

from django.db import migrations
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0027_auto_20200905_1821'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(default=None, max_length=128, null=True, unique=True),
        ),
    ]