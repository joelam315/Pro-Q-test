# Generated by Django 2.2.4 on 2020-06-26 08:18

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0004_auto_20200626_1549'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='preset_unit_price',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
