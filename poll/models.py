from django.db import models
from django.urls import reverse


class Country(models.Model):
    enabled = models.PositiveIntegerField(default=1)
    code3l = models.CharField(unique=True, max_length=3)
    code2l = models.CharField(unique=True, max_length=2)
    name = models.CharField(unique=True, max_length=64)
    name_official = models.CharField(max_length=128, blank=True, default='')
    flag_32 = models.CharField(max_length=255, blank=True, default='')
    flag_128 = models.CharField(max_length=255, blank=True, default='')
    latitude = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)
    longitude = models.DecimalField(max_digits=11, decimal_places=8, blank=True, null=True)
    zoom = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'country'

    def get_absolute_url(self):
        return reverse('poll:country', args=[self.code3l])


class CountryName(models.Model):
    country = models.ForeignKey(Country, models.CASCADE)
    code2l = models.CharField(max_length=2)
    language = models.CharField(max_length=5)
    name = models.CharField(max_length=255, blank=True, default='')
    name_official = models.CharField(max_length=255, blank=True, default='')
    source = models.CharField(max_length=255, blank=True, default='')

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'country_name'
        unique_together = (('code2l', 'language'),)


class Region(models.Model):
    name = models.CharField(max_length=32, blank=True, default='')
    is_unep = models.IntegerField()

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['name']
        db_table = 'region'


class CountryRegion(models.Model):
    country = models.ForeignKey(Country, models.CASCADE)
    region = models.ForeignKey(Region, models.CASCADE)

    class Meta:
        db_table = 'country_region'
        unique_together = (('country', 'region'),)


class ScoreRecord(models.Model):
    email = models.EmailField()
    score = models.PositiveIntegerField(default=0)
    date = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.score}: {self.email}({self.date})"
