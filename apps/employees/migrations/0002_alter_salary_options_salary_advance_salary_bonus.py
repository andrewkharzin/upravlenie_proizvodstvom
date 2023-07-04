# Generated by Django 4.2.1 on 2023-07-03 14:47

from decimal import Decimal
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='salary',
            options={'verbose_name_plural': 'Зарплаты'},
        ),
        migrations.AddField(
            model_name='salary',
            name='advance',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
        migrations.AddField(
            model_name='salary',
            name='bonus',
            field=models.DecimalField(decimal_places=2, default=Decimal('0.00'), max_digits=10),
        ),
    ]
