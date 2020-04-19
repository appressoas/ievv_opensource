from django.http import HttpResponseRedirect
from django.utils import translation
from django.utils.deprecation import MiddlewareMixin
from . import ievv_i18n_url_utils


class LocaleMiddleware(MiddlewareMixin):
    """
    `ievv_js_i18n_url` locale middleware.
    """
    response_redirect_class = HttpResponseRedirect

    def is_supported_language_code(self, request, language_code):
        """
        Check if the language code is supported by the domain.
        """
        if request.ievv_pageframework_domain.supported_languagecodes:
            if language_code in request.ievv_pageframework_domain.supported_languagecodes:
                return True
        return False

    def process_request(self, request):
        """
        Simply checks if there is a language code added as prefix to ``request.path``
        and sets this as the language for translation if it's supported by the domain.

        Args:
            request: The request-object.
        """
        handler = ievv_i18n_url_utils.get_handler(request)
        default_languagecode = handler.find_default_languagecode()
        if handler.is_translatable_urlpath(request.path):
            current_languagecode = handler.find_current_languagecode()
            if not current_languagecode or not handler.is_supported_languagecode(current_languagecode):
                current_languagecode = default_languagecode
        else:
            current_languagecode = default_languagecode

        translation.activate(current_languagecode)
        translation_language = translation.get_language()
        request.LANGUAGE_CODE = translation_language
        request.IEVV_I18N_URL_DEFAULT_LANGUAGE_CODE = default_languagecode
        request.session['LANGUAGE_CODE'] = translation_language
        return request

    def process_response(self, request, response):
        language = translation.get_language()
        if 'Content-Language' not in response:
            response['Content-Language'] = language
        return response
