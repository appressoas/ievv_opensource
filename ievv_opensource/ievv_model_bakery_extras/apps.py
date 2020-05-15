from django.apps import AppConfig
from ievv_opensource.ievv_model_bakery_extras import postgres_field_generators


class ModelBakeryExtrasAppConfig(AppConfig):
    name = 'ievv_opensource_ievv_model_bakery_extras'
    verbose_name = 'IEVV model bakery extras'

    def ready(self):
        postgres_field_generators.add_to_baker()
