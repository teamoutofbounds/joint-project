from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
from django.views.generic.list import ListView
# from users.views import LoginView

from . import views
from storageApp import settings

urlpatterns = [
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('magatzem/', include('magatzem.urls')),
    path('oficina/', include('oficina.urls')),
    path('redirect/', views.redirect_view, name='redirect-login'),
]
