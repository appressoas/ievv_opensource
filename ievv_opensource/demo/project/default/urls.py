from __future__ import unicode_literals

from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from ievv_opensource.demo.project.default.views.demo_overview import DemoView
from django_cradmin.superuserui import superuserui_registry


urlpatterns = patterns(
    '',
    url(r'^authenticate/', include('django_cradmin.apps.cradmin_authenticate.urls')),
    url(r'^resetpassword/', include('django_cradmin.apps.cradmin_resetpassword.urls')),
    url(r'^activate_account/', include('django_cradmin.apps.cradmin_activate_account.urls')),
    url(r'^register/', include('django_cradmin.apps.cradmin_register_account.urls')),

    url(r'^djangoadmin/', include(admin.site.urls)),
    url(r'^cradmin_temporaryfileuploadstore/', include('django_cradmin.apps.cradmin_temporaryfileuploadstore.urls')),
    url(r'^$', DemoView.as_view()),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT}),

    url(r'^superuser/', include(superuserui_registry.default.make_cradmin_instance_class().urls())),
)
