# Generated by Django 2.2.4 on 2020-10-12 11:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_expenses', '0005_auto_20200927_0403'),
    ]

    operations = [
        migrations.AddField(
            model_name='projectexpense',
            name='img_upload_date',
            field=models.DateField(null=True),
        ),
    ]
