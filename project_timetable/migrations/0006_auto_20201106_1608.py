# Generated by Django 2.2.4 on 2020-11-06 08:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_timetable', '0005_auto_20201106_1556'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectmilestone',
            name='img_height',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='projectmilestone',
            name='img_width',
            field=models.PositiveIntegerField(default=1),
        ),
    ]