# Generated by Django 2.1.2 on 2018-10-15 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setlists', '0004_song_show'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='show',
        ),
        migrations.AddField(
            model_name='show',
            name='songs',
            field=models.ManyToManyField(to='setlists.Song'),
        ),
    ]
