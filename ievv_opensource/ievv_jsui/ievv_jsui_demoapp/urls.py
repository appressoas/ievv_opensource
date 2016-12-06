from django.conf.urls import url
from ievv_opensource.ievv_jsui.ievv_jsui_demoapp import views

urlpatterns = [
    url(r'^$',
        views.Overview.as_view(),
        name="ievv_jsui_demo_overview"),
    url(r'^date-time-picker-demo$',
        views.DateTimePickerDemo.as_view(),
        name="ievv_jsbase_datetimepicker_demo"),
    url(r'^select-demo$',
        views.SelectDemo.as_view(),
        name="ievv_jsbase_select_demo")
]
