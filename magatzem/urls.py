# els links de l'aplicació van aqui
# els de frontend, heu d'utilitzar les funcions de views que tenen la paraula mock

from django.urls import path, include

from magatzem.views import RoomList, RoomDetail, NotificationsListView
from . import views

urlpatterns = [
    path('gestor/', views.home_gestor, name='gestor-home'),
    path('operaris/', views.home_operari, name='operaris-home'),
    path('gestor/sales/', RoomList.as_view(), name='list-room'),
    path('gestor/sales/<int:pk>/', RoomDetail.as_view(), name='detail-room'),
    # path('gestor/entrades/new/', views.exemple_mock, name='new-arrival'),
    # path('gestor/moviments/new/', views.exemple_mock, name='new-movement'),
    # path('gestor/sortides/new', views.exemple_mock, name='new-exit'),
    path('entrada_mock/', views.entrada_producte_mock, name='entrada_mock'),
    path('llista_sales_mock/', views.llista_sales_mock, name='llista-sales-mock'),
    path('sala_mock/', views.sala_mock, name='sala_mock'),
    path('operari/pepe-lopez/', views.rebre_notificacio_mock, name='notificacio-mock'),
    path('operari/user/', NotificationsListView.as_view(), name='notificacio'),
    path('sel_sala_mock/', views.seleccionar_sala_mock, name='sel-sala-mock'),
    path('sel_prod_mock/', views.seleccionar_productes_mock, name='sel-prod-mock'),
    path('tasques_mock/', views.panel_tasks_mock, name='tasques-mock'),
    path('entrada/', views.entrada_producte, name='entrada'),
]
