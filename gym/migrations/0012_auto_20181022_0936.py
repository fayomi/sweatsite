# Generated by Django 2.1 on 2018-10-22 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0011_workout_workout_description'),
    ]

    operations = [
        migrations.AlterField(
            model_name='workout',
            name='sessions',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
