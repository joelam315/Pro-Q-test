# Generated by Django 2.2.4 on 2020-10-14 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0003_auto_20201014_1522'),
    ]

    operations = [
        migrations.AddField(
            model_name='subscriptionplan',
            name='is_active',
            field=models.BooleanField(default=True),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='subscriptionplan',
            name='visible',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
    ]