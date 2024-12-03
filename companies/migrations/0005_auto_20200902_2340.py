# Generated by Django 2.2.4 on 2020-09-02 15:40

import companies.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0004_auto_20200709_1950'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentHeaderInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tel', models.CharField(blank=True, max_length=20, null=True)),
                ('email', models.EmailField(blank=True, max_length=254, null=True)),
                ('fax', models.CharField(blank=True, max_length=20, null=True)),
                ('address', models.CharField(blank=True, max_length=512, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='InvoiceGeneralRemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='QuotationGeneralRemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='ReceiptGeneralRemark',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.PositiveIntegerField()),
                ('content', models.TextField()),
            ],
        ),
        migrations.AddField(
            model_name='company',
            name='br_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='company',
            name='job_no',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='company',
            name='sign',
            field=models.FileField(blank=True, max_length=1000, null=True, upload_to=companies.models.sign_url),
        ),
        migrations.AlterField(
            model_name='company',
            name='name',
            field=models.CharField(max_length=64, verbose_name='Name'),
        ),
        migrations.DeleteModel(
            name='GeneralRemark',
        ),
        migrations.AddField(
            model_name='receiptgeneralremark',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_receipt_general_remarks', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='quotationgeneralremark',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_quotation_general_remarks', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='invoicegeneralremark',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company_invoice_general_remarks', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='documentheaderinformation',
            name='company',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='company_doc_header', to='companies.Company'),
        ),
    ]