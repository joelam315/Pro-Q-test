# Generated by Django 2.2.4 on 2020-10-28 08:01

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0017_auto_20201027_2137'),
    ]

    operations = [
        migrations.AlterField(
            model_name='itemtype',
            name='item_type_materials',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
    ]
