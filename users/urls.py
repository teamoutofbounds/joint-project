from django.urls import path, include
from django.contrib.auth import views as auth_views
from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from . import views
from storageApp import settings

urlpatterns = [
    url(r'^login/$', auth_views.LoginView.as_view(template_name="magatzem/login.html"),name='login'),
    url(r'^logout/$', LogoutView.as_view(), {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
    path('magatzem/', include('magatzem.urls')),
    path('oficina/', include('oficina.urls')),
    url(r'^exemples/$', views.exemple_mock, name='exemples'),# proba per login/logout
    url(r'^register/$', views.signup, name='register'),
]
