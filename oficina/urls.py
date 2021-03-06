from django.urls import path

from oficina import views
from oficina.views import HomeCEO, ManifestList,ManifestDetail

urlpatterns = [
    path('ceo/', HomeCEO.as_view(), name='ceo-home'),
    path('ceo/manifests', ManifestList.as_view(), name='manifests-ceo'),
    path('ceo/manifests/<int:pk>', ManifestDetail.as_view(), name='manifests-detail-ceo'),
    path('ceo/users/list/', views.list_users, name='list_users'),
    path('ceo/users/create/', views.create_user_as_ceo, name='create-user-ceo'),
    path('ceo/users/delete/<int:pk>/confirm', views.delete_user_as_ceo, name='delete-user-ceo'),
    path('ceo/sla-control', views.controlSla, name='sla-control')
]