# Generated by Django 2.1 on 2018-11-12 18:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_details', '0006_auto_20181111_2050'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='externalaccount',
            name='name',
        ),
    ]
