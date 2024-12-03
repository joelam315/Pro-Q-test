# Generated by Django 2.2.4 on 2021-01-08 07:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0027_roomitem_item_quantifier'),
    ]

    operations = [
        migrations.RenameField(
            model_name='roomitem',
            old_name='material_unit_price',
            new_name='material_value_based_price',
        ),
        migrations.AlterField(
            model_name='roomitem',
            name='quantity',
            field=models.DecimalField(decimal_places=2, max_digits=12),
        ),
    ]