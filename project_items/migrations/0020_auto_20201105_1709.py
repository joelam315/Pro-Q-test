# Generated by Django 2.2.4 on 2020-11-05 09:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('project_items', '0019_auto_20201105_1536'),
    ]

    operations = [
        migrations.AlterField(
            model_name='item',
            name='item_properties',
            field=models.ManyToManyField(blank=True, null=True, related_name='property_related_items', to='project_items.ItemProperty'),
        ),
    ]
