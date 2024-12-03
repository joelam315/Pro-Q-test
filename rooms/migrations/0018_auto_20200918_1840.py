# Generated by Django 2.2.4 on 2020-09-18 10:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0017_auto_20200918_1523'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomproperty',
            name='custom_property_formulas',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='roomproperty',
            name='property_formulas',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]