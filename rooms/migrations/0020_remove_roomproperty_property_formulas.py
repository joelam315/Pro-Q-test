# Generated by Django 2.2.4 on 2020-10-06 06:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0019_auto_20200929_1857'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='roomproperty',
            name='property_formulas',
        ),
    ]