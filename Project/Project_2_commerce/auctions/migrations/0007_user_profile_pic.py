# Generated by Django 3.2.6 on 2021-08-30 08:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20210829_2201'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='profile_pic',
            field=models.ImageField(blank='True', null='True', upload_to=''),
            preserve_default='True',
        ),
    ]
