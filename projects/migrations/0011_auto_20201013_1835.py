# Generated by Django 2.2.4 on 2020-10-13 10:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0010_auto_20201012_1832'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companyprojectcomparison',
            name='projects',
            field=models.ManyToManyField(blank=True, related_name='compared_project_record', to='projects.Project'),
        ),
    ]
