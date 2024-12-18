# Generated by Django 2.2.4 on 2021-02-01 10:52

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0029_auto_20210201_1747'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomproperty',
            name='custom_properties',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='roomproperty',
            name='custom_property_formulas',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='roomtype',
            name='room_type_formulas',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]
