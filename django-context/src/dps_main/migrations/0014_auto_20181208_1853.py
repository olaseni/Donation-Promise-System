# Generated by Django 2.1.4 on 2018-12-08 18:53

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dps_main', '0013_auto_20181207_1900'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cause',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='contact',
            options={'ordering': ['-created']},
        ),
        migrations.AlterModelOptions(
            name='promise',
            options={'ordering': ['-created']},
        ),
    ]
