# Generated by Django 3.2.6 on 2021-09-06 08:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0025_rename_status_auction_list_is_open'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watchlist',
            name='owner',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='watchlists', to=settings.AUTH_USER_MODEL),
        ),
    ]
