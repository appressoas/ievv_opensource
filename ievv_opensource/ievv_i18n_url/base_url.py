from django.utils.functional import cached_property
import urllib.parse
from ievv_opensource.ievv_i18n_url.i18n_url_settings import get_fallback_base_url_setting


class BaseUrl:
    """
    Defines ievv_i18n_url base url.

    The base URL is the URL to the root of the domain e.g: https://example.com, http://www.example.com:8080, etc.
    (NOT https://example.com/my/path, https://example.com/en, etc.).

    The constructor can take any valid absolute URL, or None
    (in which case it falls back on the IEVV_I18N_URL_FALLBACK_BASE_URL setting),
    but all the methods and properties work on a ``urllib.parse.ParseResult`` that
    does not have any of the URL parts after
    """
    def __init__(self, url_or_urllib_parseresult):
        self.url_or_urllib_parseresult = url_or_urllib_parseresult or get_fallback_base_url_setting()

    @cached_property
    def parsed_url(self):
        if isinstance(self.url_or_urllib_parseresult, urllib.parse.ParseResult):
            parsed_url = self.url_or_urllib_parseresult
        else:
            parsed_url = urllib.parse.urlparse(self.url_or_urllib_parseresult)
        return urllib.parse.ParseResult(
            scheme=parsed_url.scheme,
            netloc=parsed_url.netloc,
            path='', params='', query='', fragment='')

    @property
    def scheme(self):
        return self.parsed_url.scheme

    @property
    def netloc(self):
        return self.parsed_url.netloc

    @property
    def hostname(self):
        return self.parsed_url.hostname

    @property
    def port(self):
        return self.parsed_url.port

    def build_absolute_url(self, path_or_url):
        return urllib.parse.urljoin(self.parsed_url.geturl(), path_or_url)
