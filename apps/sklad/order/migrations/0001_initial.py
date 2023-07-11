# Generated by Django 4.2.3 on 2023-07-11 11:54

import apps.sklad.order.models.customer_class
import apps.sklad.order.models.order_class
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import mptt.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('materials', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_type', models.CharField(choices=[('Ч', 'Частный клиент'), ('К', 'Контрагент')], default='', max_length=1)),
                ('registered_year', models.IntegerField(default=2023)),
                ('counter', models.IntegerField(default=0, editable=False)),
                ('image', models.ImageField(default='customers/images/default_image.png', upload_to=apps.sklad.order.models.customer_class.customer_image_directory_path)),
                ('name', models.CharField(max_length=120, verbose_name='ФИО Клиента')),
                ('city', models.CharField(blank=True, max_length=20, null=True, verbose_name='Город')),
                ('street', models.CharField(blank=True, max_length=50, null=True, verbose_name='Улица')),
                ('phone', models.CharField(blank=True, max_length=15, null=True, verbose_name='Телефон контактный')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_type', models.CharField(choices=[('изготовление памятника', 'Изготовление памятника'), ('комплекс', 'Комплекс')], max_length=30, verbose_name='Тип заказа')),
                ('deadline', models.DateField(blank=True, null=True, verbose_name='Срок услуги')),
                ('epitaph', models.TextField(blank=True, null=True, verbose_name='Эпитафия')),
                ('description', models.TextField(blank=True, null=True, verbose_name='Детали заказа')),
                ('order_date', models.DateField(default=django.utils.timezone.now)),
                ('order_number', models.CharField(editable=False, max_length=6, unique=True)),
                ('order_status', models.CharField(choices=[('заказ принят', 'Заказ принят'), ('передан в работу', 'Передан в работу'), ('изготовление', 'Изготовление'), ('изготовлено', 'Изготовлено'), ('работы выполнены', 'Работы выполнены')], default='новый заказ', max_length=80)),
                ('qr_code_image', models.ImageField(blank=True, editable=False, null=True, upload_to='orders/qr_codes/')),
                ('create_at', models.DateTimeField(auto_now=True)),
                ('update_at', models.DateTimeField(auto_now_add=True)),
                ('customer', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='customer_order', to='order.customer')),
            ],
            options={
                'verbose_name': 'Заказ',
                'verbose_name_plural': 'Заказы',
            },
        ),
        migrations.CreateModel(
            name='OrderFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('order_file', models.FileField(upload_to=apps.sklad.order.models.order_class.order_file_path)),
                ('file_description', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='files', to='order.order')),
            ],
        ),
        migrations.CreateModel(
            name='OrderStuff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('stuff_image', models.ImageField(blank=True, null=True, upload_to=apps.sklad.order.models.order_class.order_file_path)),
                ('image_description', models.CharField(blank=True, max_length=255, null=True)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stuff', to='order.order')),
            ],
            options={
                'verbose_name': 'Файл картинки',
                'verbose_name_plural': 'Файлы картинок',
            },
        ),
        migrations.CreateModel(
            name='Shipping',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=100)),
                ('city', models.CharField(max_length=50)),
                ('state', models.CharField(max_length=50)),
                ('postal_code', models.CharField(max_length=20)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='shipping', to='order.order')),
            ],
            options={
                'verbose_name': 'Доставка',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Название услуги')),
                ('icon', models.ImageField(blank=True, null=True, upload_to='services/icons')),
                ('initial_cost', models.DecimalField(decimal_places=2, default='10.0', max_digits=10, verbose_name='Базовая цена')),
                ('price_for_work', models.DecimalField(decimal_places=2, default='0.0', max_digits=10, verbose_name='Учетная цена')),
                ('percentage_from_base', models.DecimalField(decimal_places=2, default=0, max_digits=5, verbose_name='Percentage')),
                ('lft', models.PositiveIntegerField(editable=False)),
                ('rght', models.PositiveIntegerField(editable=False)),
                ('tree_id', models.PositiveIntegerField(db_index=True, editable=False)),
                ('level', models.PositiveIntegerField(editable=False)),
                ('parent', mptt.fields.TreeForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='order.service')),
            ],
            options={
                'verbose_name': 'Наминклатура услуг',
                'verbose_name_plural': 'Наминклатура услуг',
            },
        ),
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('method', models.CharField(choices=[('наличные', 'Наличные'), ('банковской картой', 'Банковской картой'), ('банковский перевод', 'Банковский перевод')], default='Наличные', max_length=50)),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('transaction_id', models.CharField(blank=True, max_length=100, null=True)),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='payment', to='order.order')),
            ],
            options={
                'verbose_name_plural': 'Способ оплаты',
            },
        ),
        migrations.CreateModel(
            name='Passport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_number_series', models.CharField(max_length=4, verbose_name='Серия паспорта')),
                ('passport_number', models.CharField(max_length=6, verbose_name='Номер паспорта')),
                ('passport_issued_by', models.CharField(max_length=100, verbose_name='Кем выдан паспорт')),
                ('passport_issue_date', models.DateField(verbose_name='Дата выдачи паспорта')),
                ('division_code', models.CharField(max_length=7, verbose_name='Код подразделения')),
                ('customer', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='order.customer')),
            ],
            options={
                'verbose_name': 'Паспорт',
                'verbose_name_plural': 'Паспорта клиентов',
            },
        ),
        migrations.CreateModel(
            name='OrderStuffFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file_description', models.CharField(max_length=255)),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.order')),
                ('order_file', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderfile')),
                ('order_stuff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.orderstuff')),
            ],
            options={
                'verbose_name': 'Order Stuff File',
                'verbose_name_plural': 'Order Stuff Files',
            },
        ),
        migrations.AddField(
            model_name='orderstuff',
            name='stuff_files',
            field=models.ManyToManyField(through='order.OrderStuffFile', to='order.orderfile'),
        ),
        migrations.CreateModel(
            name='OrderService',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('price', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Стоимость')),
                ('quantity', models.PositiveIntegerField(verbose_name='Количество')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_services', to='order.order')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='order.service')),
            ],
            options={
                'verbose_name_plural': 'Заказанные услуги',
            },
        ),
        migrations.CreateModel(
            name='OrderMaterial',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(default=1)),
                ('material', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='materials.material')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='order_materials', to='order.order')),
            ],
            options={
                'verbose_name': 'Материал',
                'verbose_name_plural': 'Материалы',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='materials',
            field=models.ManyToManyField(related_name='order_materials', through='order.OrderMaterial', to='materials.material'),
        ),
        migrations.AddField(
            model_name='order',
            name='order_stuff',
            field=models.ManyToManyField(related_name='order_stuff_set', through='order.OrderStuffFile', to='order.orderstuff'),
        ),
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(through='order.OrderService', to='order.service'),
        ),
        migrations.CreateModel(
            name='Invoice',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(default=django.utils.timezone.now, verbose_name='Дата')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, null=True, verbose_name='Итого к оплате')),
                ('advance_payment', models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Авансовый платеж')),
                ('balance_due', models.DecimalField(decimal_places=2, default=0, editable=False, max_digits=10, verbose_name='Остаток к оплате')),
                ('bill_closed', models.BooleanField(default=False)),
                ('invoice_number', models.CharField(default='', editable=False, max_length=20, unique=True)),
                ('customer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='order.customer')),
                ('order', models.OneToOneField(on_delete=django.db.models.deletion.PROTECT, to='order.order')),
            ],
            options={
                'verbose_name': 'Счет',
                'verbose_name_plural': 'Счета',
            },
        ),
    ]
