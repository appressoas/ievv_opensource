from django.apps import AppConfig
from django_cradmin import javascriptregistry
from ievv_opensource.ievv_jsui.ievv_jsui_demoapp import static_components


class IevvJsUiDemoAppConfig(AppConfig):
    name = 'ievv_opensource.ievv_jsui.ievv_jsui_demoapp'
    verbose_name = "IEVV JsUi DemoApp"

    def ready(self):
        javascriptregistry.Registry.get_instance().add(
            static_components.IevvJsUiDemoComponent)
