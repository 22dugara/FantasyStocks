# Generated by Django 4.2.13 on 2024-05-23 04:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('leagues', '0006_league_next_week_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='leaguemembership',
            name='losses',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leaguemembership',
            name='ties',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='leaguemembership',
            name='wins',
            field=models.IntegerField(default=0),
        ),
    ]
