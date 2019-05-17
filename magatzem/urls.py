# els links de l'aplicació van aqui
# els de frontend, heu d'utilitzar les funcions de views que tenen la paraula mock
from django.urls import path
from magatzem.views import RoomList, RoomDetail, NotificationsListView, HomeGestor, TaskPanelOperaris, HomeCEO, \
    ContainerSelectionList
from . import views

urlpatterns = [
    # urls gestor
    path('gestor/', HomeGestor.as_view(), name='gestor-home'),
    # path('ceo/', views.home_ceo, name='ceo-home'),
    path('ceo/', HomeCEO.as_view(), name='ceo-home'),
    path('ceo/users/list/', views.list_users, name='list_users'),
    path('ceo/users/create/', views.create_user_as_ceo, name='create-user-ceo'),
    path('ceo/users/delete/(?P<pk>\d+)/$', views.delete_user_as_ceo, name='delete-user-ceo'),
    path('gestor/sales/', RoomList.as_view(), name='list-room'),
    path('gestor/sales/<int:pk>/', RoomDetail.as_view(), name='detail-room'),
    path('gestor/sales/<int:pk>/<room>/', ContainerSelectionList.as_view(), name='product-room'),
    path('gestor/tasques_operaris/', TaskPanelOperaris.as_view(), name='panel-operaris'),
    path('gestor/entrada/', views.manifest_form, name='entrada-producte'),
    path('gestor/sortida/', views.manifest_sortida_form, name='sortida-producte'),
    path('gestor/entrada/manifest/', views.entrada_producte, name='entrada-manifest'),
    path('gestor/sortida/manifest/', views.sortida_producte, name='sortida-manifest'),
    # urls operari
    path('operaris/notificacions/', NotificationsListView.as_view(), name='operaris-notificacions'),

    # urls tecnics

    # urls mocks
    # path('gestor/entrades/new/', views.exemple_mock, name='new-arrival'),
    # path('gestor/moviments/new/', views.exemple_mock, name='new-movement'),
    # path('gestor/sortides/new', views.exemple_mock, name='new-exit'),
    path('ceo/manifest_mock', views.manifest_list_mock, name='manifest-list-mock'),
    path('entrada_mock/', views.entrada_producte_mock, name='entrada_mock'),
    path('llista_sales_mock/', views.llista_sales_mock, name='llista-sales-mock'),
    path('sala_mock/', views.sala_mock, name='sala_mock'),
    path('operari/pepe-lopez/', views.rebre_notificacio_mock, name='notificacio-mock'),
    path('sel_sala_mock/', views.seleccionar_sala_mock, name='sel-sala-mock'),
    path('sel_prod_mock/', views.seleccionar_productes_mock, name='sel-prod-mock'),
    path('tasques_mock/', views.panel_tasks_mock, name='tasques-mock'),
    path('tasques_tecnics/', views.panel_tecnics_tasks_mock, name='tasques-tecnics-mock'),
]
