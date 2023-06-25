from django.urls import path, include
from . import views

app_name = 'estimation'
urlpatterns = [
    path('', views.EstimationView.as_view(), name="estimation"),
]