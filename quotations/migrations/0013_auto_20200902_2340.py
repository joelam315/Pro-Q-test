# Generated by Django 2.2.4 on 2020-09-02 15:40

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('quotations', '0012_auto_20200622_1554'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='quotation',
            name='function_items',
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='sub_function_items',
        ),
        migrations.RemoveField(
            model_name='quotationhistory',
            name='function_items',
        ),
        migrations.RemoveField(
            model_name='quotationhistory',
            name='sub_function_items',
        ),
    ]
