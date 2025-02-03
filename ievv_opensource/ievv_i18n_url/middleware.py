from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin

from ievv_opensource.ievv_i18n_url import active_i18n_url_translation

from . import i18n_url_utils


class LocaleMiddleware:
    """
    `ievv_js_i18n_url` locale middleware for Django 5+.
    """

    response_redirect_class = HttpResponseRedirect

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Process the request
        handler_class = i18n_url_utils.get_handler_class()
        handler_class.activate_languagecode_from_request(request=request)

        translation_language = translation.get_language()
        request.LANGUAGE_CODE = translation_language
        request.session["LANGUAGE_CODE"] = translation_language
        request.IEVV_I18N_URL_DEFAULT_LANGUAGE_CODE = (
            active_i18n_url_translation.get_default_languagecode()
        )
        request.IEVV_I18N_URL_ACTIVE_LANGUAGE_CODE = (
            active_i18n_url_translation.get_active_languagecode()
        )

        # Call the next middleware or the view
        response = self.get_response(request)

        # Process the response
        language = translation.get_language()
        if "Content-Language" not in response.headers:
            response.headers["Content-Language"] = language

        return response
