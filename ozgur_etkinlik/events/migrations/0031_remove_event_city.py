# Generated by Django 2.2.1 on 2019-07-05 15:31

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('events', '0030_auto_20190630_2225'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='event',
            name='city',
        ),
    ]