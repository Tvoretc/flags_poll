# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Country(models.Model):
    enabled = models.PositiveIntegerField(default = True)
    code3l = models.CharField(unique=True, max_length=3)
    code2l = models.CharField(unique=True, max_length=2)
    name = models.CharField(unique=True, max_length=64)
    name_official = models.CharField(max_length=128, blank=True, null=True)
    flag_32 = models.CharField(max_length=255, blank=True, null=True)
    flag_128 = models.CharField(max_length=255, blank=True, null=True)
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    zoom = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'country'


class CountryName(models.Model):
    country = models.ForeignKey(Country, models.DO_NOTHING)
    code2l = models.CharField(max_length=2)
    language = models.CharField(max_length=5)
    name = models.CharField(max_length=255, blank=True, null=True)
    name_official = models.CharField(max_length=255, blank=True, null=True)
    source = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'country_name'
        unique_together = (('code2l', 'language'),)


class Region(models.Model):
    name = models.CharField(max_length=32, blank=True, null=True)
    is_unep = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'region'


class CountryRegion(models.Model):
    country = models.ForeignKey(Country, models.DO_NOTHING)
    region = models.ForeignKey(Region, models.DO_NOTHING)

    class Meta:
        db_table = 'country_region'
        unique_together = (('country', 'region'),)
