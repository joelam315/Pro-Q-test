# Generated by Django 2.2.4 on 2021-01-13 13:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0028_auto_20210113_2105'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimageset',
            name='project_milestone',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='project_timetable.ProjectMilestone'),
        ),
    ]
