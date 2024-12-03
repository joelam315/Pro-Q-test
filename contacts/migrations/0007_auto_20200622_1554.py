# Generated by Django 2.2.4 on 2020-06-22 07:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('contacts', '0006_contact_profile_pic'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contact',
            name='address',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='address_contacts', to='common.Address'),
        ),
    ]