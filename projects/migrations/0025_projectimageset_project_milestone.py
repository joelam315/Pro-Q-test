# Generated by Django 2.2.4 on 2021-01-13 13:04

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_timetable', '0009_auto_20201120_0256'),
        ('projects', '0024_remove_projectimageset_project_milestone'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectimageset',
            name='project_milestone',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_milestone_img_set', to='project_timetable.ProjectMilestone'),
        ),
    ]
