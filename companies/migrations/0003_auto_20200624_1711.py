# Generated by Django 2.2.4 on 2020-06-24 09:11

import django.contrib.postgres.fields
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0002_auto_20200624_1701'),
    ]

    operations = [
        migrations.AlterField(
            model_name='chargingstages',
            name='descriptions',
            field=django.contrib.postgres.fields.ArrayField(base_field=models.TextField(blank=True), size=99),
        ),
    ]
