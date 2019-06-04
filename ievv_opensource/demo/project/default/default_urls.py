from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()
admin.site.login = login_required(admin.site.login)


default_urls = [
    url(r'^cradmin_authenticate/', include('django_cradmin.apps.cradmin_authenticate.urls')),
    url(r'^cradmin_resetpassword/', include('django_cradmin.apps.cradmin_resetpassword.urls')),
    url(r'^cradmin_activate_account/', include('django_cradmin.apps.cradmin_activate_account.urls')),
    url(r'^cradmin_register_account/', include('django_cradmin.apps.cradmin_register_account.urls')),
    url(r'^djangoadmin/', admin.site.urls),
    url(r'^django-rq/', include('django_rq.urls'))
]
