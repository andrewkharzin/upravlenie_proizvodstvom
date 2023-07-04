# Generated by Django 4.2.1 on 2023-07-03 16:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0005_salary_code'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='workshift',
            options={},
        ),
        migrations.RemoveField(
            model_name='workshift',
            name='end_time',
        ),
        migrations.RemoveField(
            model_name='workshift',
            name='start_time',
        ),
        migrations.AddField(
            model_name='workshift',
            name='calendar_event',
            field=models.CharField(blank=True, max_length=100, verbose_name='Событие'),
        ),
        migrations.AddField(
            model_name='workshift',
            name='end_date',
            field=models.DateField(blank=True, null=True, verbose_name='Окончание'),
        ),
        migrations.AddField(
            model_name='workshift',
            name='planned_schedule',
            field=models.TextField(blank=True, null=True, verbose_name='Планируемый график'),
        ),
        migrations.AddField(
            model_name='workshift',
            name='shift_type',
            field=models.CharField(choices=[('day', 'Day Shift'), ('night', 'Night Shift')], default='day', max_length=10, verbose_name='Режим'),
        ),
        migrations.AddField(
            model_name='workshift',
            name='start_date',
            field=models.DateField(blank=True, null=True, verbose_name='Начало'),
        ),
        migrations.AddField(
            model_name='workshift',
            name='vacation',
            field=models.BooleanField(default=False, verbose_name='Отпуск'),
        ),
    ]
