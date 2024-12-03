# Generated by Django 2.2.4 on 2020-09-02 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('project_expenses', '0002_auto_20200706_1637'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projectexpense',
            name='expend_type',
        ),
        migrations.AddField(
            model_name='projectexpense',
            name='expense_type',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.PROTECT, related_name='type_related_expense', to='project_expenses.ExpenseType'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='projectexpense',
            name='pic',
            field=models.CharField(blank=True, max_length=50, null=True, verbose_name='Person in charge'),
        ),
        migrations.AlterField(
            model_name='projectexpense',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='project_expense', to='projects.Project'),
        ),
    ]