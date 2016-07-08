import elasticsearch

from ievv_opensource.demo.project.default.settings import *  # noqa

LOCALE_PATHS = ['test_locale']

ROOT_URLCONF = 'ievv_opensource.demo.project.test.urls'
IEVV_ELASTICSEARCH_TESTURL = 'http://localhost:9251'
IEVV_ELASTICSEARCH_TESTMODE = True


IEVV_ELASTICSEARCH2_CONNECTION_ALIASES = {
    'default': {
        'host': '127.0.0.1',
        'port': '9251',
        'transport_class': 'ievv_opensource.ievv_elasticsearch2.transport.debug.DebugTransport'
    }
}
IEVV_ELASTICSEARCH2_DEBUGTRANSPORT_PRETTYPRINT_ALL_REQUESTS = True
