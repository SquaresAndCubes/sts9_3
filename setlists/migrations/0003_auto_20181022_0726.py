# Generated by Django 2.1.2 on 2018-10-22 07:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('setlists', '0002_showlist'),
    ]

    operations = [
        migrations.AlterField(
            model_name='showlist',
            name='shows',
            field=models.ManyToManyField(blank=True, to='setlists.Show'),
        ),
    ]
