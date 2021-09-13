# Generated by Django 3.2.6 on 2021-09-05 06:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0016_rename_comment_comments_parent_comment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comments',
            name='listing',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='comments', to='auctions.auction_list'),
        ),
    ]