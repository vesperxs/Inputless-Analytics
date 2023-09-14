# -*- encoding: utf-8 -*-
from django.contrib import admin
from django.urls import path, include, re_path
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    path('admin/defender/', include('defender.urls')), # defender admin
    path("", include("authentication.urls")),  # add this
    path("", include("app.urls")), # add this
    path("", include("accounts.urls")), # add this
    path("", include("upload.urls")),
    path("", include("search.urls")),
    path("search/", include('haystack.urls')),
    path("", include("payments.urls")), # add this
    path('', include('ticket.urls')), # new
    path('', include('dashboard.urls')), # new
    path('', include('sendmail.urls')), # new
    path("stripe/", include("djstripe.urls", namespace="djstripe")),
    re_path(r'^celery-progress/', include('celery_progress.urls')),
    path("", include('django_prometheus.urls')),
    path('chat/', include('chat.urls')),  # new
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
