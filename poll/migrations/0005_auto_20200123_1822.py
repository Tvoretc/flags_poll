# Generated by Django 2.2.1 on 2020-01-23 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0004_auto_20200123_1819'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scorerecord',
            name='score',
            field=models.PositiveIntegerField(default=0),
        ),
    ]
