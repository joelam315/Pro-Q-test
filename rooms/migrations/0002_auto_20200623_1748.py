# Generated by Django 2.2.4 on 2020-06-23 09:48

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomTypeProperties',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_properties', models.ManyToManyField(blank=True, to='rooms.RoomProperty')),
                ('room_type', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, related_name='room_type_properties', to='rooms.RoomType')),
            ],
        ),
        migrations.RemoveField(
            model_name='room',
            name='height',
        ),
        migrations.RemoveField(
            model_name='room',
            name='length',
        ),
        migrations.RemoveField(
            model_name='room',
            name='width',
        ),
        migrations.AddField(
            model_name='room',
            name='type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, to='rooms.RoomType'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='room',
            name='value',
            field=django.contrib.postgres.fields.jsonb.JSONField(default=None),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='RoomTypeProperty',
        ),
    ]
