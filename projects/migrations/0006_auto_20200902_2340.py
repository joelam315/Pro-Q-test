# Generated by Django 2.2.4 on 2020-09-02 15:40

import django.contrib.postgres.fields.jsonb
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0005_project_document_format'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProjectInvoice',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_on', models.DateTimeField(auto_now_add=True)),
                ('invoice_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='ProjectReceipt',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('generated_on', models.DateTimeField(auto_now_add=True)),
                ('receipt_id', models.PositiveIntegerField()),
            ],
        ),
        migrations.RemoveField(
            model_name='projecthistory',
            name='function_items',
        ),
        migrations.RemoveField(
            model_name='projecthistory',
            name='sub_function_items',
        ),
        migrations.AddField(
            model_name='project',
            name='invoice_remarks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='job_no',
            field=models.PositiveIntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='project',
            name='quotation_generated_on',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='quotation_no',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='quotation_remarks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='receipt_remarks',
            field=django.contrib.postgres.fields.jsonb.JSONField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='project',
            name='updated_on',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProjectChargingStages',
        ),
        migrations.AddField(
            model_name='projectreceipt',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AddField(
            model_name='projectinvoice',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='projects.Project'),
        ),
        migrations.AlterUniqueTogether(
            name='projectreceipt',
            unique_together={('project', 'receipt_id')},
        ),
        migrations.AlterUniqueTogether(
            name='projectinvoice',
            unique_together={('project', 'invoice_id')},
        ),
    ]
