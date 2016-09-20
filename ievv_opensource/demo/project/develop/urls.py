from django.conf.urls import url, include
from ievv_opensource.demo.project.default.default_urls import default_urls

urlpatterns = [
      url(r'^reactjs_demo/', include('ievv_opensource.demo.reactjs_demo.urls')),
] + default_urls
