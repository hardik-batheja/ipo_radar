from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('populate-data/', views.populate_data, name='populate_data'),
]
