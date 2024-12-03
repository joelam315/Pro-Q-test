# Generated by Django 2.2.4 on 2020-10-15 10:30

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0008_auto_20201014_1718'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='companysubscribedplan',
            options={'ordering': ('-start_date',)},
        ),
        migrations.AlterField(
            model_name='companysubscribedplan',
            name='start_date',
            field=models.DateField(default=datetime.datetime.now),
        ),
    ]