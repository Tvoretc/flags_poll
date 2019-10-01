from django.contrib import admin
from poll.models import Country, CountryName, Region, CountryRegion

# Register your models here.

admin.site.register(Country)
admin.site.register(CountryName)
admin.site.register(Region)
admin.site.register(CountryRegion)
