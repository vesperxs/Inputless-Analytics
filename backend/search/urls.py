from django.urls import path
from . import views

urlpatterns = [
    path('multiscope_views', views.multiscope_views, name='multiscope_views'),
    path('procid_views', views.procid_views, name='procid_views'),
    path('decrid_views', views.decrid_views, name='decrid_views'),
    path('art_views', views.art_views, name='art_views'),
    path('cass_views', views.cass_views, name='cass_views'),
    path('table_views', views.table_views, name='table_views'),
    path('filter_results', views.filter_results, name='filter_results'),
]
