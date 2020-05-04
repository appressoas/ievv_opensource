from django.conf.urls import include, url
from ievv_opensource.demo.project.default.default_urls import default_urls


urlpatterns = [
    url(r'^ievv_i18n_url_testapp/', include('ievv_opensource.ievv_i18n_url.tests.ievv_i18n_url_testapp.urls'))
] + default_urls
