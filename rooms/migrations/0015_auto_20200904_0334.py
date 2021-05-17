# Generated by Django 2.2.4 on 2020-09-03 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rooms', '0014_auto_20200904_0030'),
    ]

    operations = [
        migrations.AddField(
            model_name='roomtypeformula',
            name='is_active',
            field=models.BooleanField(default=True),
        ),
        migrations.AlterField(
            model_name='roomproperty',
            name='data_type',
            field=models.CharField(choices=[('Boolean', 'bool'), ('Number', 'num')], max_length=50),
        ),
    ]
