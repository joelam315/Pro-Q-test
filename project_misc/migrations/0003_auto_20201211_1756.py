# Generated by Django 2.2.4 on 2020-12-11 09:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_misc', '0002_auto_20201120_0256'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='misc',
            options={'ordering': ['-id'], 'verbose_name': 'Misc', 'verbose_name_plural': 'Misc'},
        ),
    ]