from django.conf.urls import include, url
from django.contrib import admin
from django.contrib.auth.decorators import login_required

admin.autodiscover()
admin.site.login = login_required(admin.site.login)


default_urls = [
    url(r'^cradmin_authenticate/', include('cradmin_legacy.apps.cradmin_authenticate.urls')),
    url(r'^cradmin_temporaryfileuploadstore/', include('cradmin_legacy.apps.cradmin_temporaryfileuploadstore.urls')),
    url(r'^cradmin_resetpassword/', include('cradmin_legacy.apps.cradmin_resetpassword.urls')),
    url(r'^cradmin_activate_account/', include('cradmin_legacy.apps.cradmin_activate_account.urls')),
    url(r'^cradmin_register_account/', include('cradmin_legacy.apps.cradmin_register_account.urls')),
    url(r'^djangoadmin/', admin.site.urls),
    url(r'^django-rq/', include('django_rq.urls')),
    # url(r'^ievv_elasticsearch2browser/', include('ievv_opensource.ievv_elasticsearch2browser.urls')),
]
