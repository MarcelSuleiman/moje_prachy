# Generated by Django 3.2.11 on 2022-01-19 20:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0009_items_ean'),
    ]

    operations = [
        migrations.AlterField(
            model_name='items',
            name='item_class',
            field=models.CharField(blank=True, default='bez kategorie', max_length=100),
        ),
        migrations.AlterField(
            model_name='items',
            name='item_sub_class',
            field=models.CharField(blank=True, default='bez podkategorie', max_length=100),
        ),
    ]
