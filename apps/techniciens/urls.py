
from django.urls import path
from . import views
app_name = 'techniciens'
urlpatterns = [
    path('', views.liste_techniciens, name='liste'),
]
