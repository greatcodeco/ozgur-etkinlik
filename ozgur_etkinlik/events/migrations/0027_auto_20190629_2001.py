# Generated by Django 2.2.1 on 2019-06-29 17:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('events', '0026_auto_20190629_1957'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='starter_date',
            field=models.DateField(blank=True, null=True, verbose_name='Başlangıç günü'),
        ),
    ]
