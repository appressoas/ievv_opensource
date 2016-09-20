from django.conf.urls import url
from ievv_opensource.demo.reactjs_demo.views import simpleview

urlpatterns = [
    url(r'simple$', simpleview.SimpleDemoView.as_view()),
]
