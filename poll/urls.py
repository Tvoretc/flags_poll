from django.urls import path
from poll import views

app_name = 'poll'

urlpatterns = [
    path('', views.pollView, name = 'poll'),
    path('result/', views.pollResultView, name = 'result'),
    path('list/', views.countriesByRegionsView, name = 'list_by_regions'),
    path('generic/', views.CountryListView.as_view(), name = 'generic'),
    path('country/<str:code3>', views.countryView, name = 'country'),
]
