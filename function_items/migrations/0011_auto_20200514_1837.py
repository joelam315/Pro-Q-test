# Generated by Django 2.2.4 on 2020-05-14 10:37

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('function_items', '0010_auto_20200514_1812'),
    ]

    operations = [
        migrations.CreateModel(
            name='FunctionItemHistory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('Frotn-end', 'Front-end'), ('Back-end', 'Back-end'), ('System', 'System'), ('Design', 'Design')], default='Front-end', max_length=20)),
                ('status', models.CharField(choices=[('Requested', 'Requested'), ('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Approved', 'Approved')], default='Requested', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('function_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='function_item_history', to='function_items.FunctionItem')),
                ('updated_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='function_item_history_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['type', '-created_on'],
            },
        ),
        migrations.DeleteModel(
            name='VersionValue',
        ),
    ]
