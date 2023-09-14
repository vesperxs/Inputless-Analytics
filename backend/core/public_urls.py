from django.contrib import admin
from django.urls import path, include, re_path

from django.conf import settings
from django.conf.urls.static import static

from two_factor.urls import urlpatterns as tf_urls



urlpatterns = [
    path('admin/', admin.site.urls),
    path("", include("home_public.urls")),
    path('', include(tf_urls)),
    path('admin/defender/', include('defender.urls')), # defender admin
    path("", include("registration.urls")), # add this
    path("", include('django_prometheus.urls')),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
