from django.db import models

from ievv_opensource.utils.singleton import Singleton


class Registry(Singleton):
    def __init__(self):
        self.anonymize_handlers = {}
        self.datatype_handlers = {}
        super().__init__()

    def set_anonymize_handler(self, anonymize_handler_class):
        self.anonymize_handlers[anonymize_handler_class.get_registry_id()] = anonymize_handler_class

    def set_datatype_handler(self, datatype_handler_class):
        self.anonymize_handlers[datatype_handler_class.get_registry_id()] = datatype_handler_class

    def get_default_handler_class(self):
        raise NotImplementedError()

    def anonymize(self, data, handler_id=None, datatype_map=None):
        anonymize_handler_class = None
        if handler_id:
            anonymize_handler_class = self.anonymize_handlers[handler_id]
        elif isinstance(data, models.Model):
            handler_id = data._meta.label
            anonymize_handler_class = self.anonymize_handlers.get(handler_id, None)
        if anonymize_handler_class is None:
            anonymize_handler_class = self.get_default_handler_class()
        return anonymize_handler_class(data=data, datatype_map=datatype_map).anonymize()
