from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from . import i18n_url_utils


class LocaleMiddleware(MiddlewareMixin):
    """
    `ievv_js_i18n_url` locale middleware.
    """
    response_redirect_class = HttpResponseRedirect

    def process_request(self, request):
        """
        Initializes the ievv_i18n_url handler from the request,
        and calls :meth:`ievv_opensource.ievv_i18n_url.handlers.abstract_handler.activate_detected_languagecode`.

        Args:
            request: The request-object.
        """
        handler = i18n_url_utils.get_handler(request)
        handler.activate_detected_languagecode()
        return request

    def process_response(self, request, response):
        language = translation.get_language()
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
