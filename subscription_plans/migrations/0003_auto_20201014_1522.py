# Generated by Django 2.2.4 on 2020-10-14 07:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0002_auto_20201014_1520'),
    ]

    operations = [
        migrations.AlterField(
            model_name='companysubscribedplan',
            name='end_date',
            field=models.DateField(blank=True, null=True),
        ),
    ]