# Generated by Django 3.2.11 on 2022-01-19 20:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0008_auto_20220119_1411'),
    ]

    operations = [
        migrations.AddField(
            model_name='items',
            name='ean',
            field=models.CharField(blank=True, max_length=13),
        ),
    ]
