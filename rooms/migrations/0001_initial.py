# Generated by Django 2.2.4 on 2020-06-22 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='RoomProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='RoomTypeFormula',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('formula', models.TextField()),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rooms.RoomType')),
            ],
        ),
        migrations.CreateModel(
            name='Room',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('length', models.PositiveIntegerField()),
                ('width', models.PositiveIntegerField()),
                ('height', models.PositiveIntegerField()),
                ('related_project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_rooms', to='projects.Project')),
            ],
        ),
        migrations.CreateModel(
            name='RoomTypeProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('room_property', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rooms.RoomProperty')),
                ('room_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='rooms.RoomType')),
            ],
            options={
                'unique_together': {('room_type', 'room_property')},
            },
        ),
    ]
