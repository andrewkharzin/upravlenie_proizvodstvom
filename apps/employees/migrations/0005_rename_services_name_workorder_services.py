# Generated by Django 4.2.3 on 2023-07-11 12:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('employees', '0004_alter_workorderservice_service'),
    ]

    operations = [
        migrations.RenameField(
            model_name='workorder',
            old_name='services_name',
            new_name='services',
        ),
    ]