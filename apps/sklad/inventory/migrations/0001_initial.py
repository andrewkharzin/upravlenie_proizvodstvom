# Generated by Django 4.2.3 on 2023-07-07 04:54

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True)),
                ('date_created', models.DateTimeField(default=django.utils.timezone.now)),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('reason', models.CharField(choices=[('первичная', 'Первиная'), ('повторная', 'Повторная'), ('Списание', 'Списание')], max_length=20)),
            ],
            options={
                'verbose_name_plural': 'Инвентаризация',
            },
        ),
        migrations.CreateModel(
            name='InventoryItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('received_quantity', models.IntegerField(default=0)),
                ('received_date', models.DateTimeField(auto_now_add=True)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='items', to='inventory.inventory')),
                ('received_by', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='received_items', to=settings.AUTH_USER_MODEL)),
                ('responsible_person', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='responsible_items', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Позиции',
            },
        ),
        migrations.CreateModel(
            name='InventoryHistory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_modified', models.DateTimeField(auto_now=True)),
                ('reason', models.CharField(choices=[('первичная', 'Первиная'), ('повторная', 'Повторная'), ('Списание', 'Списание')], max_length=20)),
                ('inventory', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='history_entries', to='inventory.inventory')),
            ],
            options={
                'verbose_name_plural': 'Трэкинг',
            },
        ),
    ]
