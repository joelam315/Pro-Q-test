# Generated by Django 2.2.4 on 2020-10-14 09:13

import colorfield.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0006_auto_20201014_1702'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='bg_color',
            field=colorfield.fields.ColorField(default='#FFFFFF', max_length=18),
        ),
    ]
