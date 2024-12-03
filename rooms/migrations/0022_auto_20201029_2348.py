# Generated by Django 2.2.4 on 2020-10-29 15:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0018_auto_20201028_1601'),
        ('rooms', '0021_auto_20201012_1715'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomitem',
            name='material_s',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='material_related_project_items', to='project_items.ItemTypeMaterial'),
        ),
        migrations.AlterField(
            model_name='roomitem',
            name='material',
            field=models.TextField(blank=True, null=True),
        ),
    ]