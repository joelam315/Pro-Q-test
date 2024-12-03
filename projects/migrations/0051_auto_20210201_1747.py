# Generated by Django 2.2.4 on 2021-02-01 09:47

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0050_auto_20210118_1810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='projectimageset',
            name='project_milestone',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_milestone_img_set', to='project_timetable.ProjectMilestone'),
        ),
    ]