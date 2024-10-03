# Generated by Django 4.2.11 on 2024-10-03 08:13

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0013_listing_won_listings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='listing',
            name='won_listings',
        ),
        migrations.AddField(
            model_name='listing',
            name='won',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
