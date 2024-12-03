# Generated by Django 2.2.4 on 2020-10-27 06:45

import companies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0011_auto_20201027_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='br_pic_height',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AddField(
            model_name='company',
            name='br_pic_width',
            field=models.PositiveIntegerField(blank=True, default=0, null=True),
        ),
        migrations.AlterField(
            model_name='company',
            name='br_pic',
            field=models.FileField(blank=True, max_length=1000, null=True, upload_to=companies.models.br_url),
        ),
    ]