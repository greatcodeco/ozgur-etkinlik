# Generated by Django 2.2.1 on 2019-06-11 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0019_newcomment'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='starter_time',
            field=models.TimeField(null=True, verbose_name='Başlangıç saati'),
        ),
        migrations.AlterField(
            model_name='event',
            name='starter_date',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Başlangıç günü'),
        ),
    ]