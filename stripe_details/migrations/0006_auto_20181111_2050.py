# Generated by Django 2.1 on 2018-11-11 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('stripe_details', '0005_auto_20181110_1946'),
    ]

    operations = [
        migrations.RenameField(
            model_name='company',
            old_name='legal_entity_typebusiness_tax_id',
            new_name='legal_entity_type_business_tax_id',
        ),
        migrations.RemoveField(
            model_name='company',
            name='companies_house_registration_number_CRN',
        ),
        migrations.AddField(
            model_name='company',
            name='legal_entity_dob_day',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='legal_entity_dob_month',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='legal_entity_dob_year',
            field=models.PositiveIntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='legal_entity_first_name',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='company',
            name='legal_entity_last_name',
            field=models.CharField(default='none', max_length=100),
            preserve_default=False,
        ),
    ]