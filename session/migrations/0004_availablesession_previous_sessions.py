# Generated by Django 2.1 on 2018-10-22 08:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('session', '0003_auto_20181021_1728'),
    ]

    operations = [
        migrations.AddField(
            model_name='availablesession',
            name='previous_sessions',
            field=models.IntegerField(default=0),
        ),
    ]
