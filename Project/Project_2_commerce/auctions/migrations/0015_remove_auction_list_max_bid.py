# Generated by Django 3.2.6 on 2021-09-01 10:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0014_alter_bids_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='auction_list',
            name='max_bid',
        ),
    ]
