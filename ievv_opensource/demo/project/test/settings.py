from ievv_opensource.demo.project.default.settings import *  # noqa


ROOT_URLCONF = 'ievv_opensource.demo.project.test.urls'

INSTALLED_APPS += [
    'ievv_opensource.ievv_i18n_url.tests.ievv_i18n_url_testapp',
]
