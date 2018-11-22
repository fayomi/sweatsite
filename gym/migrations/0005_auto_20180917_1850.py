# Generated by Django 2.1 on 2018-09-17 18:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0004_auto_20180917_1813'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='clientprofile',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
        migrations.AddField(
            model_name='trainerprofile',
            name='first_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='trainerprofile',
            name='last_name',
            field=models.CharField(max_length=30, null=True),
        ),
        migrations.AddField(
            model_name='trainerprofile',
            name='slug',
            field=models.SlugField(max_length=250, null=True, unique=True),
        ),
    ]