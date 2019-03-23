# els links de l'aplicació van aqui
# els de frontend, heu d'utilitzar les funcions de views que tenen la paraula mock

from django.urls import path
from . import views

urlpatterns = [
    path('exemples/', views.exemple_mock, name='exemple'),
    path('entrada_mock/', views.entrada_producte_mock, name='entrada_mock')
]
