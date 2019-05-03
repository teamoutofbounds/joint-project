from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView
# from users.views import LoginView

from . import views
from storageApp import settings

urlpatterns = [
    # path('', LoginView.as_view(template_name='users/login.html'), name='login'),
    path('', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='users/logout.html'), name='logout'),
    path('magatzem/', include('magatzem.urls')),
    path('oficina/', include('oficina.urls')),
    # path('register/', views.signup, name='register'),
    path('redirect/', views.redirect_view, name='redirect-login'),
]
