from . import views
from .views import ProgressBarUploadView
from django.urls import path
from django.views.generic import TemplateView
from django.contrib.admin.views.decorators import staff_member_required


urlpatterns = [
    path('clear', views.clear_database, name='clear_database'),
    path('progress-bar-upload', staff_member_required(ProgressBarUploadView.as_view()), name='progress_bar_upload'),
    path('analyze', views.analyze, name='analyze'),
    path('reindex', views.reindex, name='reindex'),
]
