# Generated by Django 2.2.4 on 2020-07-06 08:57

import django.contrib.postgres.fields.jsonb
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0002_projectchargingstages'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='charging_stages',
            field=django.contrib.postgres.fields.jsonb.JSONField(default='[]'),
            preserve_default=False,
        ),
    ]
