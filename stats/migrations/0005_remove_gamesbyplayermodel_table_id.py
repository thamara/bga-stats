# Generated by Django 3.2.6 on 2021-09-06 00:54

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0004_auto_20210905_2044'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='gamesbyplayermodel',
            name='table_id',
        ),
    ]
