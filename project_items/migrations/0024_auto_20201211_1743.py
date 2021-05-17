# Generated by Django 2.2.4 on 2020-12-11 09:43

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0023_auto_20201211_1329'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_formulas',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
        migrations.AlterField(
            model_name='itemtype',
            name='item_type_materials',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, default=list, null=True),
        ),
    ]
