# Generated by Django 2.2.4 on 2020-12-11 05:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0022_auto_20201105_1852'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='itemtype',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='itemtypematerial',
            options={'ordering': ['-id']},
        ),
    ]