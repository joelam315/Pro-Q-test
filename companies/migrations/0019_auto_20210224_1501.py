# Generated by Django 2.2.4 on 2021-02-24 07:01

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0018_auto_20210224_1313'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='gen_invoice_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='gen_invoice_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='company',
            name='gen_quot_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='gen_quot_date',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='company',
            name='gen_receipt_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='company',
            name='gen_receipt_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]