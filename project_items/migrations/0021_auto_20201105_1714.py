# Generated by Django 2.2.4 on 2020-11-05 09:14

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0020_auto_20201105_1709'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'ordering': ['-id'], 'verbose_name': 'Item', 'verbose_name_plural': 'Items'},
        ),
    ]
