# Generated by Django 2.2.4 on 2020-10-21 09:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('subscription_plans', '0010_auto_20201019_1718'),
    ]

    operations = [
        migrations.RenameField(
            model_name='companysubscribedplan',
            old_name='end_date',
            new_name='next_billing_date',
        ),
    ]