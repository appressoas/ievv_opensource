from urllib import parse

from django.conf import settings
from django.urls import reverse
from django.utils.module_loading import import_string


class FakeHttpRequest:
    """
    A fake Django HttpRequest that can be used wherever `ievv_i18n_url`
    requires a ``request`` argument.

    This is mostly to support management scripts or background tasks that do not
    have access to an HttpRequest.

    Also serves to define what attributes of HttpRequest the `ievv_i18n_url`
    library uses.

    WARNING: If you create a custom handler you may not be able to use this if you
    use parts of HttpRequest that this "fake" class does not support.
    """
    def __init__(self, absolute_url, language_code, default_languagecode, **extra_request_attributes):
        """

        Args:
            absolute_url (str): The absolute URL - e.g.: ``https://www.mydomain.com/path/to/my/view?x=2&y=3``.
            language_code (str): The language code.
            default_languagecode (str): The default language code.
            **extra_request_attributes: Extra attributes to set on the request. Should be used to set
                application specific attributes, not attributes that exist on HttpRequest like ``session``.
        """
        self.absolute_url = absolute_url
        self.LANGUAGE_CODE = language_code
        self.IEVV_I18N_URL_DEFAULT_LANGUAGE_CODE = default_languagecode
        # self.parsed_url = urlparse(self.absolute_url)
        self.session = {
            "LANGUAGE_CODE": self.LANGUAGE_CODE
        }

    def build_absolute_uri(self, path=None):
        if path is None:
            return self.absolute_url
        return parse.urljoin(self.absolute_url, path)


_handler_class = None


def get_handler(request):
    """
    Get the configured `ievv_i18n_url` handler.

    E.g. import the handler class from the class path configured in the ``IEVV_I18N_URL_HANDLER`` setting.

    Args:
        request (django.http.HttpRequest): Django http request object, or a
            :class:`ievv_opensource.ievv_i18n_url.ievv_i18n_url_utils.FakeHttpRequest` object.

    Returns:
        ievv_opensource.ievv_i18n_url.i18n_url_handlers.abstract_handler.AbstractHandler: A handler object.
    """
    global _handler_class
    if _handler_class is None:
        handler_classpath = getattr(settings, 'IEVV_I18N_URL_HANDLER', None)
        if not handler_classpath:
            raise Exception(
                'No ievv_i18n_url_handler configured. Please set the IEVV_I18N_URL_HANDLER. Refer to the docs for '
                'ievv_i18n_url in ievv_opensource for more info.')
        _handler_class = import_string(handler_classpath)
    return _handler_class(request)


def i18n_reverse(request, viewname, urlconf=None, args=None, kwargs=None, current_app=None, languagecode=None):
    """
    Serves kind of the same use case as the ``django.urls.reverse`` function, but with i18n URL support, AND
    this function returns an absolute URL.

    The reason why it returns absolute URL is because i18n URLs may be based on domains, not just URL paths.

    NOTE: Session based `ievv_i18n_url` handlers will ignore the languagecode argument and just return
    the URL for the default translation. This is because all their translations live at the same URL.
    See the _A warning about session based translations_ in the docs for more details.

    Args:
        request (django.http.HttpRequest): Django http request object, or a
            :class:`ievv_opensource.ievv_i18n_url.ievv_i18n_url_utils.FakeHttpRequest` object.
        viewname: See the docs for ``django.urls.reverse``.
        urlconf: See the docs for ``django.urls.reverse``. Defaults to None.
        args: See the docs for ``django.urls.reverse``. Defaults to None.
        kwargs: See the docs for ``django.urls.reverse``. Defaults to None.
        current_app: See the docs for ``django.urls.reverse``. Defaults to None.
        languagecode (str, optional): The languagecode to reverse the URL in. Defaults to None, which means
            we reverse the URL in the current languagecode.

    Returns:
        str: An URL.
    """
    path = reverse(viewname=viewname, urlconf=urlconf, args=args, kwargs=kwargs, current_app=current_app)
    return get_handler(request).build_absolute_url(path=path, languagecode=languagecode)


def transform_url_to_languagecode(request, uri, to_languagecode, from_languagecode=None):
    """Takes an URL, and finds the URL to the same content within a different languagecode.

    NOTE: Session based `ievv_i18n_url` handlers will ignore the languagecode argument and just return
    provided uri. This is because all their translations live at the same URL.
    See the _A warning about session based translations_ in the docs for more details.

    Args:
        request ([type]): [description]
        uri (str): The URL to transform.
        to_languagecode (str): The languagecode to transform the uri into.
        from_languagecode (str): The languagecode to transform the uri from.

    Returns:
        str: The transformed URL. If from_languagecode and to_languagecode is the same,
            the provided ``uri`` is returned unchanged.
    """
    return get_handler(request).transform_url_to_languagecode(uri=uri, to_languagecode=to_languagecode)
