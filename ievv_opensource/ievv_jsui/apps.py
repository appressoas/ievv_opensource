from django.apps import AppConfig
from django_cradmin import javascriptregistry
from ievv_opensource.ievv_jsui import static_components


class IevvJsUiAppConfig(AppConfig):
    name = 'ievv_opensource.ievv_jsui'
    verbose_name = "IEVV jsui"

    def ready(self):
        javascriptregistry.Registry.get_instance().add(
            static_components.IevvJsUiCoreComponent)
