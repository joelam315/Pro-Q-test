# Generated by Django 2.2.4 on 2020-10-12 09:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0020_remove_roomproperty_property_formulas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='roomproperty',
            name='data_type',
            field=models.CharField(choices=[('bool', 'Boolean'), ('num', 'Number'), ('string', 'String'), ('custom property', 'Custom Property')], max_length=50),
        ),
    ]
