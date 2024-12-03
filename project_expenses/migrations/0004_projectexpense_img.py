# Generated by Django 2.2.4 on 2020-09-20 07:22

from django.db import migrations, models
import project_expenses.models


class Migration(migrations.Migration):

    dependencies = [
        ('project_expenses', '0003_auto_20200902_2340'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectexpense',
            name='img',
            field=models.FileField(blank=True, max_length=1000, null=True, upload_to=project_expenses.models.expense_img_url),
        ),
    ]