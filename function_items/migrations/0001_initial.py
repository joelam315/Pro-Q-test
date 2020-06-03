# Generated by Django 2.2.4 on 2020-05-06 11:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('total_amount', models.DecimalField(decimal_places=2, max_digits=12)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='function_items_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Function Item',
                'verbose_name_plural': 'Function Items',
            },
        ),
    ]
