# Generated by Django 2.1 on 2018-09-17 19:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0007_auto_20180917_1902'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientprofile',
            name='slug',
        ),
        migrations.RemoveField(
            model_name='trainerprofile',
            name='slug',
        ),
    ]