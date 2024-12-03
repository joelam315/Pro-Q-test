# Generated by Django 2.2.4 on 2020-11-06 07:56

import common.fields
import companies.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0014_auto_20201027_1646'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='br_pic_height',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='br_pic_width',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='logo_pic_height',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='logo_pic_width',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='sign_height',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='sign_width',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='company',
            name='br_pic',
            field=common.fields.EncryptedImageField(blank=True, height_field='br_pic_height', null=True, upload_to=companies.models.br_url, width_field='br_pic_width'),
        ),
        migrations.AlterField(
            model_name='company',
            name='logo_pic',
            field=common.fields.EncryptedImageField(blank=True, height_field='logo_pic_height', null=True, upload_to=companies.models.logo_url, width_field='logo_pic_width'),
        ),
        migrations.AlterField(
            model_name='company',
            name='sign',
            field=common.fields.EncryptedImageField(blank=True, height_field='sign_height', null=True, upload_to=companies.models.sign_url, width_field='sign_width'),
        ),
    ]