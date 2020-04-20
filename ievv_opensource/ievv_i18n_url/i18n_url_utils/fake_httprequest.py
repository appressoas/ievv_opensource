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
