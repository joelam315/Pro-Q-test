# Generated by Django 2.2.4 on 2020-10-14 06:53

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('companies', '0007_documentformat_project_lower_format'),
    ]

    operations = [
        migrations.CreateModel(
            name='SubscriptionPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('plan_name', models.CharField(max_length=256, verbose_name='Plan Name')),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=12, null=True)),
                ('project_quota', models.PositiveIntegerField()),
                ('function_permission', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('description', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='CompanySubscribedPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(auto_now_add=True)),
                ('end_date', models.DateField(blank=True)),
                ('company', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscription_histories', to='companies.Company')),
                ('plan', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='subscriptions', to='subscription_plans.SubscriptionPlan')),
            ],
        ),
    ]
