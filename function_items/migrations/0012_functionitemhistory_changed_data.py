# Generated by Django 2.2.4 on 2020-05-14 11:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function_items', '0011_auto_20200514_1837'),
    ]

    operations = [
        migrations.AddField(
            model_name='functionitemhistory',
            name='changed_data',
            field=models.TextField(blank=True, null=True, verbose_name='Changed Data'),
        ),
    ]