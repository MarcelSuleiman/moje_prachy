# Generated by Django 3.2.11 on 2022-01-26 00:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0013_auto_20220124_2111'),
    ]

    operations = [
        migrations.AddField(
            model_name='category',
            name='name2',
            field=models.TextField(blank=True, max_length=150, null=True),
        ),
    ]
