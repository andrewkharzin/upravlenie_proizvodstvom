# Generated by Django 4.2.3 on 2023-07-11 11:54

import apps.sklad.materials.models.material_class
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='MaterialType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
            ],
            options={
                'verbose_name': 'Тип материала',
                'verbose_name_plural': 'Типы материалов',
            },
        ),
        migrations.CreateModel(
            name='Property',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('object_id', models.PositiveIntegerField()),
                ('name', models.CharField(max_length=100)),
                ('value', models.CharField(max_length=100)),
                ('content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.contenttype')),
            ],
            options={
                'verbose_name': 'Свойство материала',
                'verbose_name_plural': 'Свойства материалов',
            },
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('image', models.ImageField(blank=True, null=True, upload_to=apps.sklad.materials.models.material_class.material_image_upload_path)),
                ('date_created', models.DateField(auto_now=True)),
                ('purchase_price', models.DecimalField(decimal_places=2, default='0.0', max_digits=10, verbose_name='Цена закупки')),
                ('material_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.materialtype')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы',
            },
        ),
    ]
