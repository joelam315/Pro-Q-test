# Generated by Django 2.2.4 on 2021-01-07 11:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0025_auto_20201120_0256'),
    ]

    operations = [
        migrations.AddField(
            model_name='room',
            name='measure_quantifier',
            field=models.CharField(choices=[('mm', 'mm'), ('m', 'm')], default='mm', max_length=20),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roomitem',
            name='material_unit_price',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=12),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='roomitem',
            name='measure_quantifier',
            field=models.CharField(choices=[('mm', 'mm'), ('m', 'm')], default='mm', max_length=20),
            preserve_default=False,
        ),
    ]
