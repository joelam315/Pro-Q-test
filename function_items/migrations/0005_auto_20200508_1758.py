# Generated by Django 2.2.4 on 2020-05-08 09:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('function_items', '0004_functionitem_price'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='functionitem',
            options={'ordering': ['type', '-created_on'], 'verbose_name': 'Function Item', 'verbose_name_plural': 'Function Items'},
        ),
    ]
