# Generated by Django 2.2.4 on 2020-07-06 09:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0003_project_charging_stages'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='function_items',
        ),
        migrations.RemoveField(
            model_name='project',
            name='sub_function_items',
        ),
        migrations.RemoveField(
            model_name='project',
            name='teams',
        ),
    ]
