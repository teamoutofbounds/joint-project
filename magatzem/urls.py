# els links de l'aplicació van aqui
# els de frontend, heu d'utilitzar les funcions de views que tenen la paraula mock

from django.urls import path, include
from . import views

urlpatterns = [
    path('exemples/', views.exemple_mock, name='exemple'),
    path('', include('django.contrib.auth.urls')), # S'han de crear usuaris
]