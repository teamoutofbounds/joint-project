# els links de l'aplicació van aqui
# els de frontend, heu d'utilitzar les funcions de views que tenen la paraula mock
from django.urls import path
from magatzem.views import RoomList, RoomDetail, NotificationsOperarisListView, HomeGestor, TaskPanelOperaris, \
    ContainerSelectionList, ConfirmNotification, TaskPanelTecnics, EditTecnicTask, DeleteTecnicTask, \
    NotificationsTecnicsListView, ConfirmNotificationTecnics, UpdateClimaRoom, OpenRoom, EntradaProducte, \
    CreateAutomatedTasks, SortidaProducte
from . import views

urlpatterns = [
    # urls gestor
    path('gestor/', HomeGestor.as_view(), name='gestor-home'),
    path('gestor/sales/', RoomList.as_view(), name='list-room'),
    path('gestor/sales/<int:pk>/', RoomDetail.as_view(), name='detail-room'),
    path('gestor/sales/<int:pk>/<room>/', ContainerSelectionList.as_view(), name='product-room'),
    # urls gestor tasques operaris
    path('gestor/tasques_operaris/', TaskPanelOperaris.as_view(), name='panel-operaris'),

    path('gestor/tasques_operaris/<int:pk>/edit/', EditTecnicTask.as_view(), name='task-tecnic-edit'),
    # urls gestor tasques tecnics
    path('gestor/tasques_tecnics/', TaskPanelTecnics.as_view(), name='panel-tecnics'),
    path('gestor/tasques_tecnics/<int:pk>/edit/', EditTecnicTask.as_view(), name='task-tecnic-edit'),
    path('gestor/tasques_tecnics/<int:pk>/delete/', DeleteTecnicTask.as_view(), name='task-tecnic-delete'),
    # urls gestor tasques magatzem
    path('gestor/entrada/', views.manifest_form, name='entrada-producte'),
    path('gestor/sortida/', views.manifest_sortida_form, name='sortida-producte'),
    path('gestor/entrada/manifest/', EntradaProducte.as_view(), name='entrada-manifest'),  # hauria de ser /new
    path('gestor/sortida/manifest/', SortidaProducte.as_view(), name='sortida-manifest'),  # hauria de ser /new
    path('gestor/entrada/manifest/confirm/<int:pk>', CreateAutomatedTasks.as_view(), name='automated-tasks'),
    # urls operari
    path('operaris/notificacions/', NotificationsOperarisListView.as_view(), name='operaris-notificacions'),
    path('operaris/notificacions/confirm/<int:pk>/', ConfirmNotification.as_view(), name='confirm-notification'),
    # urls tecnics
    path('tecnic/notificacions/', NotificationsTecnicsListView.as_view(), name='tecnics-notificacions'),
    path('tecnics/notificacions/confirm/<int:pk>/', ConfirmNotificationTecnics.as_view(),
         name='confirm-notification-tecnics'),
    # path('tecnic/', , name='tecnic-home'),

    #urls generar tasques
    path('gestor/sales/<int:pk>/clima', UpdateClimaRoom.as_view(), name='update-clima'),
    path('gestor/sales/<int:pk>/obrir', OpenRoom.as_view(), name='open-room'),

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
