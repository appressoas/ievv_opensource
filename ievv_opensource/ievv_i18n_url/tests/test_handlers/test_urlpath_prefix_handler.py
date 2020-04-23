from unittest import mock

from django import test
from ievv_opensource.ievv_i18n_url import active_i18n_url_translation
from ievv_opensource.ievv_i18n_url.base_url import BaseUrl
from ievv_opensource.ievv_i18n_url.handlers.urlpath_prefix_handler import \
    UrlpathPrefixHandler


class UrlpathPrefixExtraPrefixHandler(UrlpathPrefixHandler):
    LANGUAGECODE_URLPATH_PREFIX = 'l/s'


@test.override_settings(
    LANGUAGE_CODE='en',
    LANGUAGES=(
        ('en', 'English'),
        ('nb', 'Norwegian'),
        ('de', 'German'),
    ),
    IEVV_I18N_URL_FALLBACK_BASE_URL='https://example.com'
)
class TestAbstractHandler(test.TestCase):
    def setUp(self):
        active_i18n_url_translation.activate()

    def test_get_urlpath_prefix_for_languagecode(self):
        self.assertEqual(UrlpathPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'nb'), 'nb')
        self.assertEqual(UrlpathPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'en'), '')
        self.assertEqual(UrlpathPrefixExtraPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'en'), '')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.get_urlpath_prefix_for_languagecode(BaseUrl(), 'nb'),
            'l/s/nb')

    def test_strip_languagecode_from_urlpath(self):
        self.assertEqual(UrlpathPrefixHandler().strip_languagecode_from_urlpath('/nb/my/view'), '/my/view')
        self.assertEqual(UrlpathPrefixHandler().strip_languagecode_from_urlpath('/x/nb/my/view'), '/x/nb/my/view')
        self.assertEqual(UrlpathPrefixHandler().strip_languagecode_from_urlpath('/en/my/view'), '/my/view')
        self.assertEqual(UrlpathPrefixHandler().strip_languagecode_from_urlpath('/xx/my/view'), '/xx/my/view')

        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler().strip_languagecode_from_urlpath('/l/s/nb/my/view'),
            '/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler().strip_languagecode_from_urlpath('/x/l/s/nb/my/view'),
            '/x/l/s/nb/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler().strip_languagecode_from_urlpath('/l/s/en/my/view'),
            '/my/view')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler().strip_languagecode_from_urlpath('/l/s/xx/my/view'),
            '/l/s/xx/my/view')

    def test_get_languagecode_from_url(self):
        self.assertEqual(UrlpathPrefixHandler().get_languagecode_from_url('/nb/my/view'), 'nb')
        self.assertEqual(UrlpathPrefixHandler().get_languagecode_from_url('/x/nb/my/view'), None)
        self.assertEqual(UrlpathPrefixHandler().get_languagecode_from_url('/sv/my/view'), None)

        self.assertEqual(UrlpathPrefixExtraPrefixHandler().get_languagecode_from_url('/l/s/nb/my/view'), 'nb')
        self.assertEqual(UrlpathPrefixExtraPrefixHandler().get_languagecode_from_url('/x/l/s/nb/my/view'), None)
        self.assertEqual(UrlpathPrefixExtraPrefixHandler().get_languagecode_from_url('/l/s/sv/my/view'), None)

    def test_detect_current_languagecode(self):
        class MockRequest:
            def __init__(self, path):
                self.path = path

        self.assertEqual(
            UrlpathPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/nb/my/view')),
            'nb')
        self.assertEqual(
            UrlpathPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/x/nb/my/view')),
            None)
        self.assertEqual(
            UrlpathPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/sv/my/view')),
            None)

        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/l/s/nb/my/view')),
            'nb')
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/x/l/s/nb/my/view')),
            None)
        self.assertEqual(
            UrlpathPrefixExtraPrefixHandler.detect_current_languagecode(BaseUrl(), MockRequest('/l/s/sv/my/view')),
            None)

    def test_build_urlpath(self):
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view'),
            '/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='nb'),
            '/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='en'),
            '/my/view')

    def test_build_urlpath_nondefault_active_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='nb')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view'),
            '/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='nb'),
            '/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_urlpath('/my/view', languagecode='en'),
            '/my/view')

    def test_build_absolute_url(self):
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view'),
            'https://example.com/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='nb'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='en'),
            'https://example.com/my/view')

    def test_build_absolute_url_nondefault_active_languagecode(self):
        active_i18n_url_translation.activate(active_languagecode='nb')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='nb'),
            'https://example.com/nb/my/view')
        self.assertEqual(
            UrlpathPrefixHandler().build_absolute_url('/my/view', languagecode='en'),
            'https://example.com/my/view')
