# Generated by Django 2.2.4 on 2021-01-13 06:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0013_auto_20210112_2010'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectimage',
            options={'ordering': ['-id']},
        ),
        migrations.AlterModelOptions(
            name='projectimageset',
            options={'ordering': ['-id']},
        ),
        migrations.AddField(
            model_name='projectimage',
            name='display_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AddField(
            model_name='projectimageset',
            name='display_id',
            field=models.IntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='projectimageset',
            name='project_milestone',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='project_milestone_img_set', to='project_timetable.ProjectMilestone'),
        ),
    ]