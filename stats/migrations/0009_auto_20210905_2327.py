# Generated by Django 3.2.6 on 2021-09-06 02:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0008_auto_20210905_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesbyplayermodel',
            name='player_id',
        ),
        migrations.AddField(
            model_name='gamesbyplayermodel',
            name='player',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stats.playerdetailsmodel'),
        ),
    ]
