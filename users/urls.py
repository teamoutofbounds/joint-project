from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.contrib.auth.views import LogoutView

from . import views
from storageApp import settings

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('logout/', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('magatzem/', include('magatzem.urls')),
    path('oficina/', include('oficina.urls')),
    path('register/', views.signup, name='register'),
]
