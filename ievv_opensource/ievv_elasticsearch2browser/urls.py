from django.conf.urls import patterns, url, include

from ievv_opensource.ievv_elasticsearch2browser.cradmin import ElasticSearchBrowserCrAdminInstance

urlpatterns = patterns(
    '',
    url(r'^', include(ElasticSearchBrowserCrAdminInstance.urls())),
)
