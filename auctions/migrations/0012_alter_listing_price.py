# Generated by Django 4.2.11 on 2024-10-01 11:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0011_bid_listing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='listing',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]