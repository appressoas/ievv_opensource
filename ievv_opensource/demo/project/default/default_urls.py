from django.urls import include, path
from django.contrib import admin


admin.autodiscover()


default_urls = [
    path('', include('django.contrib.auth.urls')),
    path('djangoadmin/', admin.site.urls),
    path('django-rq/', include('django_rq.urls')),
]
