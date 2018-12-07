# Generated by Django 2.1.4 on 2018-12-07 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dps_main', '0007_cause_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cause',
            name='target_amount',
            field=models.FloatField(default=0.0, help_text='Amount promised in NGN', verbose_name='Amount promised, NGN'),
        ),
    ]
