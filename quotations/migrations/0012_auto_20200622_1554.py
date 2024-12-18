# Generated by Django 2.2.4 on 2020-06-22 07:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('function_items', '0013_auto_20200622_1554'),
        ('quotations', '0011_auto_20200518_1800'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='quotation',
            options={'ordering': ('-created_on',), 'verbose_name': 'Quotation', 'verbose_name_plural': 'Quotations'},
        ),
        migrations.AlterModelOptions(
            name='quotationhistory',
            options={'ordering': ('-created_on',)},
        ),
        migrations.RemoveField(
            model_name='quotation',
            name='accounts',
        ),
        migrations.AddField(
            model_name='quotation',
            name='companies',
            field=models.ManyToManyField(related_name='companies_quotations', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='quotation',
            name='sub_function_items',
            field=models.ManyToManyField(related_name='quotations_sub_function_items', to='function_items.SubFunctionItem'),
        ),
        migrations.AddField(
            model_name='quotationhistory',
            name='sub_function_items',
            field=models.ManyToManyField(related_name='quotations_history_sub_function_items', to='function_items.SubFunctionItemHistory'),
        ),
    ]
