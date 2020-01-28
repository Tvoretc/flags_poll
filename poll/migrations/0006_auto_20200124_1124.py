# Generated by Django 2.2.1 on 2020-01-24 09:24

from django.db import migrations
import os, json

from flags_poll.settings import BASE_DIR


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0005_auto_20200123_1822'),
    ]

    def populate_countries(apps, schema_editor):
        Country = apps.get_model('poll', 'Country')
        with open(os.path.join(BASE_DIR, 'poll', 'migrations', 'countries.json'), 'r') as file:
            data = json.load(file)
            for country in data:
                c = Country(
                    enabled = country['enabled'],
                    code3l = country['code3l'],
                    code2l = country['code2l'],
                    name = country['name'],
                    name_official = country['name_official'],
                    latitude = country['latitude'],
                    longitude = country['longitude'],
                    zoom = country['zoom'],
                )
                c.save()


    operations = [
        migrations.RunPython(populate_countries)
    ]
