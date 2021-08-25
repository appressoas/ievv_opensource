from django.urls import include, path

from ievv_opensource.demo.project.default.default_urls import default_urls
from ievv_opensource.ievv_i18n_url import i18n_url_utils

urlpatterns = i18n_url_utils.i18n_patterns(*[
    path(r'ievv_i18n_url_testapp/', include('ievv_opensource.ievv_i18n_url.tests.ievv_i18n_url_testapp.urls'))
] + default_urls)
