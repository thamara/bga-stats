# Generated by Django 3.2.6 on 2021-09-05 23:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0003_auto_20210905_1548'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesbyplayermodel',
            name='name',
        ),
        migrations.AddField(
            model_name='gamesbyplayermodel',
            name='player_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='gamesbyplayermodel',
            name='table_id',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='gamesbyplayermodel',
            name='id',
            field=models.BigAutoField(primary_key=True, serialize=False),
        ),
    ]
