# Generated by Django 2.2.4 on 2020-05-07 08:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('function_items', '0002_auto_20200507_1601'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='functionitem',
            options={'ordering': ['-created_on'], 'verbose_name': 'Function Item', 'verbose_name_plural': 'Function Items'},
        ),
        migrations.AddField(
            model_name='functionitem',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
