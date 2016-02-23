import elasticsearch

from ievv_opensource.demo.project.default.settings import *  # noqa
from ievv_opensource.ievv_es.transport.debug import DebugTransport

LOCALE_PATHS = ['test_locale']

IEVV_ELASTICSEARCH_TESTURL = 'http://localhost:9251'
IEVV_ELASTICSEARCH_TESTMODE = True


IEVV_ES_CONNECTIONS = {
    'default': {
        'host': '127.0.0.1',
        'port': '9251',
        'transport_class': 'ievv_opensource.ievv_es.transport.debug.DebugTransport'
    }
}
IEVV_ES_DEBUGTRANSPORT_PRETTYPRINT_ALL_REQUESTS = True
