from django.urls import path, include
from . import views

app_name = 'scraping'
urlpatterns = [
    path('', views.ScrapingView.as_view(), name="scraping"),
]
