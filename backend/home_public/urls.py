from django.urls import path, re_path
from . import views

from django.contrib.auth.views import LogoutView

urlpatterns = [
    re_path(r'^.*\.html', views.pages, name='pages'),
    path("", views.welcome, name="home"),
]


