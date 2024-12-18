# Generated by Django 2.2.4 on 2021-01-12 12:10

import datetime
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0012_projectimage_projectimageset'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectimage',
            name='img_upload_date',
        ),
        migrations.AddField(
            model_name='projectimageset',
            name='upload_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AlterField(
            model_name='projectimageset',
            name='project_milestone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_milestone_img_set', to='project_timetable.ProjectMilestone'),
        ),
    ]
