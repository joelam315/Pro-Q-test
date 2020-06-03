# Generated by Django 2.2.4 on 2020-05-18 10:00

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('quotations', '0010_remove_quotationhistory_total_amount'),
    ]

    operations = [
        migrations.AddField(
            model_name='quotation',
            name='approved_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotation_approved_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotation',
            name='approved_on',
            field=models.DateTimeField(null=True),
        ),
        migrations.AddField(
            model_name='quotation',
            name='last_updated_by',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='quotation_last_updated_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='quotation',
            name='last_updated_on',
            field=models.DateTimeField(auto_now_add=True, default=datetime.datetime(2020, 5, 18, 18, 0, 0, 628598)),
            preserve_default=False,
        ),
    ]