# Generated by Django 2.2.4 on 2020-06-24 08:09

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0002_auto_20200624_1609'),
        ('rooms', '0004_auto_20200623_1935'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomItem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('unit_price', models.DecimalField(decimal_places=2, default=0, max_digits=12)),
                ('value', django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True)),
                ('quantity', models.PositiveIntegerField()),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='related_project_items', to='project_items.Item')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='room_project_items', to='rooms.Room')),
            ],
            options={
                'verbose_name': 'Room Item',
                'verbose_name_plural': 'Room Items',
            },
        ),
    ]
