# Generated by Django 2.1 on 2018-10-19 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0007_orderitem_sessions'),
    ]

    operations = [
        migrations.AddField(
            model_name='orderitem',
            name='workout_description',
            field=models.TextField(default='There is no description available'),
        ),
    ]
