# Generated by Django 2.2.4 on 2020-06-22 07:54

from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    dependencies = [
        ('companies', '0001_initial'),
        ('common', '0021_auto_20200506_1732'),
    ]

    operations = [
        migrations.AddField(
            model_name='attachments',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='company_attachment', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='comment',
            name='company',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='companies_comments', to='companies.Company'),
        ),
        migrations.AddField(
            model_name='user',
            name='br_approved',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='phone',
            field=phonenumber_field.modelfields.PhoneNumberField(max_length=128, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_verify',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='user',
            name='verify_code',
            field=models.CharField(blank=True, max_length=6),
        ),
        migrations.AlterField(
            model_name='apisettings',
            name='tags',
            field=models.ManyToManyField(blank=True, to='companies.Tags'),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.EmailField(blank=True, default=None, max_length=255, null=True, unique=True),
        ),
    ]
