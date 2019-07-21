from django.urls import path
from poll import views

urlpatterns = [
    path('', views.pollView, name = 'poll'),
    path('result/', views.pollResultView, name = 'result'),
]
