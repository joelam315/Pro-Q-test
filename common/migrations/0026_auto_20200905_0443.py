# Generated by Django 2.2.4 on 2020-09-04 20:43

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('common', '0025_auto_20200902_2340'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='user',
            options={'ordering': ['-date_joined']},
        ),
    ]
