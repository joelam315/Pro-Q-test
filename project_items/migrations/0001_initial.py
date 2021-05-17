# Generated by Django 2.2.4 on 2020-06-22 07:54

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
            name='Item',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('type', models.CharField(choices=[('Frotn-end', 'Front-end'), ('Back-end', 'Back-end'), ('System', 'System'), ('Design', 'Design')], default='Front-end', max_length=20)),
                ('status', models.CharField(choices=[('Requested', 'Requested'), ('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Approved', 'Approved')], default='Requested', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='project_items_created_by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Function Item',
                'verbose_name_plural': 'Function Items',
                'ordering': ['type', '-created_on'],
            },
        ),
        migrations.CreateModel(
            name='ProjectItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Name')),
                ('price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('description', models.TextField(blank=True, null=True)),
                ('status', models.CharField(choices=[('Requested', 'Requested'), ('Pending', 'Pending'), ('Rejected', 'Rejected'), ('Approved', 'Approved')], default='Requested', max_length=20)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('created_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='sub_project_items_created_by', to=settings.AUTH_USER_MODEL)),
                ('related_item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_project_items', to='project_items.Item')),
            ],
            options={
                'verbose_name': 'Sub Function Item',
                'verbose_name_plural': 'Sub Function Items',
                'ordering': ['created_on'],
            },
        ),
    ]
