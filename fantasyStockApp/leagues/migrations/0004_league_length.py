# Generated by Django 4.2.13 on 2024-05-19 20:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0003_league_draftdone'),
    ]

    operations = [
        migrations.AddField(
            model_name='league',
            name='length',
            field=models.IntegerField(default=7),
        ),
    ]
