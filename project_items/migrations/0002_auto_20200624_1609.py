# Generated by Django 2.2.4 on 2020-06-24 08:09

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemProperty',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('symbol', models.CharField(max_length=50, unique=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('is_active', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='ItemTypeMaterial',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('item_type', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='item_type_materials', to='project_items.ItemType')),
            ],
        ),
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Item', 'verbose_name_plural': 'Items'},
        ),
        migrations.RemoveField(
            model_name='item',
            name='created_by',
        ),
        migrations.RemoveField(
            model_name='item',
            name='created_on',
        ),
        migrations.RemoveField(
            model_name='item',
            name='price',
        ),
        migrations.RemoveField(
            model_name='item',
            name='status',
        ),
        migrations.RemoveField(
            model_name='item',
            name='type',
        ),
        migrations.AddField(
            model_name='item',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.DeleteModel(
            name='ProjectItem',
        ),
        migrations.AddField(
            model_name='item',
            name='item_properties',
            field=models.ManyToManyField(blank=True, to='project_items.ItemProperty'),
        ),
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='related_items', to='project_items.ItemType'),
            preserve_default=False,
        ),
    ]
