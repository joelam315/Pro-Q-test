# Generated by Django 2.2.4 on 2021-01-13 13:43

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0036_auto_20210113_2138'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimageset',
            name='project_milestone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='project_timetable.ProjectMilestone'),
        ),
    ]
