# Generated by Django 2.2.4 on 2020-11-19 18:56

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('project_expenses', '0010_auto_20201120_0223'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projectexpense',
            options={'ordering': ['-id']},
        ),
    ]
