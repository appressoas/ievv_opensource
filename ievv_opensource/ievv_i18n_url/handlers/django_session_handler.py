from django.conf import settings
from django.utils import translation

from . import abstract_handler


class DjangoSessionHandler(abstract_handler.AbstractHandler):
    """
    Django session based i18n url handler.

    .. warning::

        Please read the *A warning about session based translations* in the docs before
        deciding to use this handler.
    """
    def build_absolute_url(self, path, languagecode=None):
        return self.request.build_absolute_uri(path)

    def transform_url_to_languagecode(self, url, languagecode):
        return url

    def find_current_languagecode(self):
        return translation.get_language_from_request(self.request)

    def find_default_languagecode(self):
        return settings.LANGUAGE_CODE
