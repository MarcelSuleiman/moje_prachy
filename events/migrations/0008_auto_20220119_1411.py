# Generated by Django 3.2.11 on 2022-01-19 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0007_auto_20220117_1655'),
    ]

    operations = [
        migrations.AddField(
            model_name='receiptsids',
            name='created_date',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created date'),
        ),
        migrations.AddField(
            model_name='receiptsids',
            name='created_time',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Created time'),
        ),
        migrations.AddField(
            model_name='receiptsids',
            name='day_name',
            field=models.CharField(blank=True, max_length=20, null=True, verbose_name='Day name'),
        ),
        migrations.AddField(
            model_name='receiptsids',
            name='seller',
            field=models.CharField(blank=True, max_length=150, null=True, verbose_name='Seller'),
        ),
        migrations.AddField(
            model_name='receiptsids',
            name='total_price',
            field=models.FloatField(blank=True, null=True, verbose_name='Total price'),
        ),
        migrations.AlterField(
            model_name='items',
            name='ico',
            field=models.CharField(blank=True, max_length=8),
        ),
        migrations.AlterField(
            model_name='items',
            name='owner',
            field=models.CharField(max_length=100),
        ),
    ]
