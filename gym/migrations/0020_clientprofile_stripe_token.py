# Generated by Django 2.1 on 2018-11-14 21:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('gym', '0019_clientprofile_stripe_customer_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientprofile',
            name='stripe_token',
            field=models.CharField(max_length=200, null=True),
        ),
    ]
