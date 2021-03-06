# Generated by Django 3.2.11 on 2022-01-12 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0003_receiptsids'),
    ]

    operations = [
        migrations.CreateModel(
            name='Items',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_of_purchase_time_stamp', models.IntegerField()),
                ('date_of_purchase', models.CharField(max_length=10)),
                ('item', models.CharField(max_length=100)),
                ('quantity', models.IntegerField()),
                ('price_per_one', models.IntegerField()),
                ('price_per_all', models.IntegerField()),
                ('vat_rate', models.IntegerField()),
                ('item_type', models.CharField(max_length=10)),
                ('seller', models.CharField(max_length=100)),
                ('uid', models.CharField(max_length=34)),
                ('ico', models.CharField(max_length=8)),
                ('cash_register_code', models.CharField(max_length=20)),
                ('issue_date', models.CharField(max_length=20)),
                ('created_date', models.CharField(max_length=20)),
                ('customer_id', models.TextField(blank=True)),
                ('dic', models.CharField(max_length=10)),
                ('ic_dph', models.CharField(max_length=12)),
                ('invoice_number', models.TextField(blank=True)),
                ('okp', models.CharField(max_length=44)),
                ('paragon', models.BooleanField()),
                ('paragon_number', models.TextField(blank=True)),
                ('pkp', models.TextField()),
                ('receipt_no', models.IntegerField()),
                ('type_receipt', models.CharField(max_length=50)),
                ('tax_base_basic', models.IntegerField()),
                ('tax_base_reduced', models.IntegerField()),
                ('total_price', models.IntegerField()),
                ('free_tax_amount', models.IntegerField()),
                ('vat_amount_basic', models.IntegerField()),
                ('vat_amount_reduced', models.IntegerField()),
                ('vat_rate_basic', models.IntegerField()),
                ('vat_rate_reduced', models.IntegerField()),
                ('owner', models.CharField(max_length=100)),
            ],
        ),
    ]
