# els links de l'aplicació van aqui
# els de frontend, heu d'utilitzar les funcions de views que tenen la paraula mock

from django.urls import path, include

from magatzem.views import RoomList, RoomDetail
from . import views

urlpatterns = [
    path('gestor/', views.exemple_mock, name='gestor-home'),
    path('operaris/', views.exemple_mock, name='operari-home'),
    # path('gestor/sales/', RoomList.as_view(), name='list-room'),
    path('gestor/sales/', views.llista_sales_mock, name='list-room'),
    path('gestor/sales/<int:pk>/', RoomDetail.as_view(), name='detail-room'),
    path('gestor/entrades/new/', views.exemple_mock, name='new-arrival'),
    path('gestor/moviments/new/', views.exemple_mock, name='new-movement'),
    path('gestor/sortides/new', views.exemple_mock, name='new-exit'),
    path('exemples/', views.exemple_mock, name='exemple'),
    path('entrada_mock/', views.entrada_producte_mock, name='entrada_mock'),
    path('llista_sales_mock/', views.llista_sales_mock, name='llista-sales_mock'),
    path('sala_mock/', views.sala_mock, name='sala_mock'),
    path('operari/pepe-lopez/', views.rebre_notificacio_mock, name='notificacio-mock')
]
