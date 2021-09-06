# Generated by Django 3.2.6 on 2021-09-05 18:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('stats', '0002_auto_20210905_1539'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlayerDetailsModel',
            fields=[
                ('id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=300)),
            ],
        ),
        migrations.AddField(
            model_name='gamesbyplayermodel',
            name='game',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='stats.gamemodel'),
        ),
        migrations.AlterField(
            model_name='gamesbyplayermodel',
            name='id',
            field=models.IntegerField(primary_key=True, serialize=False),
        ),
    ]