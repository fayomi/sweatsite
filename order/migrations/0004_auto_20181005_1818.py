# Generated by Django 2.1 on 2018-10-05 18:18

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0003_order_name'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='order',
            name='billingAddress1',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billingCity',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billingCountry',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billingName',
        ),
        migrations.RemoveField(
            model_name='order',
            name='billingPostcode',
        ),
    ]
