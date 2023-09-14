# -*- encoding: utf-8 -*-
from django.urls import path, re_path
from django.conf.urls import url, include
from app import views

from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [
    # Matches any html file 
    re_path(r'^.*\.html', views.pages, name='pages'),
    # The home page
    path('', views.index, name='home'),
    path('', include(tf_urls)),
    path('search_options', views.search_options, name='search_options'),
    path('filters', views.filters, name='filters'), 
    path('table', views.table, name='table'), 
    path('user', views.user, name='user'), 
    path('progress_bar_upload', views.progress_bar_upload, name='progress_bar_upload'),
]
