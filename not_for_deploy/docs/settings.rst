########
Settings
########


*************************
ievvtasks_dump_db_as_json
*************************

.. setting:: IEVVTASKS_DUMPDATA_DIRECTORY

IEVVTASKS_DUMPDATA_DIRECTORY
============================
The directory where we put dumps created by the ``ievvtasks_dump_db_as_json``
management command. Typically, you put something like this in your develop settings::

    THIS_DIR = os.path.dirname(__file__)

    IEVVTASKS_DUMPDATA_DIRECTORY = os.path.join(THIS_DIR, 'dumps')


.. setting:: IEVVTASKS_DUMPDATA_ADD_EXCLUDES

IEVVTASKS_DUMPDATA_ADD_EXCLUDES
===============================
Use this setting to add models and apps to exclude from the dumped json. We exclude:

- contenttypes
- auth.Permission
- sessions.Session

By default, and we exclude ``thumbnail.KVStore`` by default if ``sorl.thumbnail`` is
in installed apps, and the ``THUMBNAIL_KVSTORE`` setting is configured to use the
database (``sorl.thumbnail.kvstores.cached_db_kvstore.KVStore``).

Example::

    IEVVTASKS_DUMPDATA_ADD_EXCLUDES = [
        'auth.Group',
        'myapp.MyModel',
    ]



.. setting:: IEVVTASKS_DUMPDATA_EXCLUDES

IEVVTASKS_DUMPDATA_EXCLUDES
===========================
If you do not want to get the default excludes, you can use this instead of
:setting:`IEVVTASKS_DUMPDATA_ADD_EXCLUDES` to specify exactly what to
exclude.


**********************
ievvtasks_makemessages
**********************


.. setting:: IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES

IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES
=====================================
The languages to build translations for. Example::

    IEVVTASKS_MAKEMESSAGES_LANGUAGE_CODES = ['en', 'nb']


.. setting:: IEVVTASKS_MAKEMESSAGES_IGNORE

IEVVTASKS_MAKEMESSAGES_IGNORE
=============================
The patterns to ignore when making translations. Defaults to::

    IEVVTASKS_MAKEMESSAGES_IGNORE = [
        'static/*'
    ]


.. setting:: IEVVTASKS_MAKEMESSAGES_BUILD_JAVASCRIPT_TRANSLATIONS

IEVVTASKS_MAKEMESSAGES_BUILD_JAVASCRIPT_TRANSLATIONS
====================================================
Set this to ``True`` if you want to built translations for javascript code. Defaults to ``False``.


.. setting:: IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE

IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE
========================================
The patterns to ignore when making javascript translations. Defaults to::

    IEVVTASKS_MAKEMESSAGES_JAVASCRIPT_IGNORE = [
        'node_modules/*',
        'bower_components/*',
        'not_for_deploy/*',
    ]



**************
ievvtasks_docs
**************


.. setting:: IEVVTASKS_DOCS_DIRECTORY

IEVVTASKS_DOCS_DIRECTORY
========================
The directory where your sphinx docs resides (the directory where you have your sphinx ``conf.py``).
Defaults to ``not_for_deploy/docs/``.

.. setting:: IEVVTASKS_DOCS_BUILD_DIRECTORY

IEVVTASKS_DOCS_BUILD_DIRECTORY
==============================
The directory where your sphinx docs should be built.
Defaults to ``not_for_deploy/docs/_build``.



************************
ievvtasks_recreate_devdb
************************

.. setting:: IEVVTASKS_RECREATE_DEVDB_POST_MANAGEMENT_COMMANDS

IEVVTASKS_RECREATE_DEVDB_POST_MANAGEMENT_COMMANDS
=================================================
Iterable of managemement commands to after creating/restoring and migrating the
database in ``ievv recreate_devdb``. Example::

    IEVVTASKS_RECREATE_DEVDB_POST_MANAGEMENT_COMMANDS = [
        {
            'name': 'createsuperuser',
            'args': ['test@example.com'],
            'options': {'verbosity': 3}
        },
        'ievvtasks_set_all_passwords_to_test',
    ]

The items in the iterable can be one of:

- A string with the name of a management command (for commands without any
  arguments or options).
- A dict with ``name``, ``args``, and ``options`` keys. The
  ``name`` key is required, but ``args`` and ``options`` are
  optional. ``args`` and ``options`` is just forwarded to
  ``django.core.management.call_command``.


*****************
ievv_tagframework
*****************


.. setting:: IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES

IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES
=================================
The legal values for :obj:`ievv_opensource.ievv_tagframework.models.Tag.tagtype`.

Example::

    IEVV_TAGFRAMEWORK_TAGTYPE_CHOICES = [
        ('', ''),
        ('mytype', 'My tag type'),
    ]


***********
ievv devrun
***********

.. setting:: IEVVTASKS_DEVRUN_RUNNABLES

IEVVTASKS_DEVRUN_RUNNABLES
==========================
Dict mapping ``ievv devrun`` target names to :class:`ievv_opensource.utils.ievvdevrun.config.RunnableThreadList`
objects. Must contain the ``"default"`` key.

Documented in :doc:`ievvtask_devrun`.



******************
ievv_elasticsearch
******************


.. setting:: IEVV_ELASTICSEARCH_URL

IEVV_ELASTICSEARCH_URL
======================
The URL of the elasticsearch instance.



.. setting:: IEVV_ELASTICSEARCH_TESTURL

IEVV_ELASTICSEARCH_TESTURL
==========================
The URL where we run elasticsearch for UnitTests.
We provide a config file in ``not_for_deploy/elasticsearch.unittest.yml`` used with::

    $ elasticsearch --config=path/to/elasticsearch.unittest.yml

to configure elasticsearch in a manner suitable for Unit testing as long as this setting
is set to::

    IEVV_ELASTICSEARCH_TESTURL = 'http://localhost:9251'


.. setting:: IEVV_ELASTICSEARCH_TESTMODE

IEVV_ELASTICSEARCH_TESTMODE
===========================

Set this to True to make ElasticSearch behave in a manner that
makes writing Unit tests a bit easier:

- Automatically refresh the indexes after any index update.
- Use ``IEVV_ELASTICSEARCH_TESTURL`` instead of ``IEVV_ELASTICSEARCH_URL``.

Add the following to you test settings to enable testmode::

    IEVV_ELASTICSEARCH_TESTMODE = True


.. setting:: IEVV_ELASTICSEARCH_PRETTYPRINT_ALL_SEARCH_QUERIES

IEVV_ELASTICSEARCH_PRETTYPRINT_ALL_SEARCH_QUERIES
=================================================

Set this to True to prettyprint all ElasticSearch search queries. Defaults to ``False``.
Good for debugging.


.. setting:: IEVV_ELASTICSEARCH_PRETTYPRINT_ALL_REQUESTS

IEVV_ELASTICSEARCH_PRETTYPRINT_ALL_REQUESTS
===========================================

Set this to True to prettyprint all ElasticSearch requests (both input and output).
Defaults to ``False``. Good for debugging.


.. setting:: IEVV_ELASTICSEARCH_AUTOREFRESH_AFTER_INDEXING

IEVV_ELASTICSEARCH_AUTOREFRESH_AFTER_INDEXING
=============================================
Automatically refresh after indexing with
meth:`ievv_opensource.ievv_elasticsearch.searchindex.AbstractIndex.index_items`.
Useful for unit tests, but not much else.

You **should not** add this to your test settings, but use it in your
tests where appropriate like this::

    class MyTestCase(TestCase):
        def test_something(self):
            with self.settings(IEVV_ELASTICSEARCH_AUTOREFRESH_AFTER_INDEXING=False):
                # test something here



.. setting:: IEVV_ELASTICSEARCH_DO_NOT_REGISTER_INDEX_UPDATE_TRIGGERS

IEVV_ELASTICSEARCH_DO_NOT_REGISTER_INDEX_UPDATE_TRIGGERS
========================================================
Do not register index update triggers on Django startup? Defaults to ``False``.
Mostly useful during development.


.. setting:: IEVV_ELASTICSEARCH_MAJOR_VERSION

IEVV_ELASTICSEARCH_MAJOR_VERSION
================================
The major version of elasticsearch you are using. Defaults to ``1``, but we also
support ``2``.



*******************
ievv_elasticsearch2
*******************

.. setting:: IEVV_ELASTICSEARCH2_CONNECTION_ALIASES

IEVV_ELASTICSEARCH2_CONNECTION_ALIASES
======================================
Setup elasticsearch connections (almost exactly like setting up Django databases). Example::

    IEVV_ELASTICSEARCH2_CONNECTION_ALIASES = {
        'default': {
            'host': '127.0.0.1',
            'port': '9251'
        },
        'theother': {
            'host': '127.0.0.1',
            'port': '9254'
        }
    }

The inner dict (the one with host and port) are kwargs for
:class:`elasticsearch.client.Elasticsearch`. These configurations
are all registered with :class:`elasticsearch_dsl.connections.Connections`.
This means that you can call ``elasticsearch_dsl.connections.connections.get_connection(alias=<alias>)``
to get an :class:`elasticsearch.client.Elasticsearch` object with the configured connection
settings::

    from elasticsearch_dsl.connections import connections

    default_elasticsearch = connections.get_connection()  # defaults to alias="default"
    theother_elasticsearch = connections.get_connection(alias="theother")

Elasticsearch-dsl also uses :class:`elasticsearch_dsl.connections.Connections`, so this
means that you can use these aliases with :meth:`elasticsearch_dsl.search.Search.using`
and :meth:`ievv_opensource.ievv_elasticsearch2.search.Search.using`::

    from ievv_opensource import ievv_elasticsearch2

    result = ievv_elasticsearch2.Search()\
        .query('match', name='Peter')\
        .using('theother')
        .execute()

.. note:: The ``IEVV_ELASTICSEARCH2_CONNECTION_ALIASES`` setting only works if you add
    ``ievv_elasticsearch2`` to ``INSTALLED_APPS`` with the AppConfig::

        INSTALLED_APPS = [
            # .. Other apps ...
            "ievv_opensource.ievv_elasticsearch2.apps.IevvEsAppConfig",
        ]


.. setting:: IEVV_ELASTICSEARCH2_DEBUGTRANSPORT_PRETTYPRINT_ALL_REQUESTS

IEVV_ELASTICSEARCH2_DEBUGTRANSPORT_PRETTYPRINT_ALL_REQUESTS
===========================================================
If this is ``True``, it makes :class:`ievv_opensource.ievv_elasticsearch2.transport.debug.DebugTransport`
prettyprint all requests performed by any :class:`elasticsearch.client.Elasticsearch`
object it is configured as the ``transport_class`` for.

This does not work unless you use :class:`ievv_opensource.ievv_elasticsearch2.transport.debug.DebugTransport`
as the transport class. This is easiest to achieve by just adding it to your
:setting:`IEVV_ELASTICSEARCH2_CONNECTION_ALIASES` setting::

    IEVV_ELASTICSEARCH2_CONNECTION_ALIASES = {
        'default': {
            'host': '<somehost>',
            'port': '<someport>',
            'transport_class': 'ievv_opensource.ievv_elasticsearch2.transport.debug.DebugTransport'
        }
    }

You may want to set this to ``True`` to just see all elasticsearch requests and responses,
but you can also use this in tests to debug just some requests::

    class MyTest(TestCase):
        def test_something(self):
            # ... some code here ...
            with self.settings(IEVV_ELASTICSEARCH2_DEBUGTRANSPORT_PRETTYPRINT_ALL_REQUESTS=True):
                # ... some elasticsearch queries here ...
            # ... more code here ...


*****
utils
*****

.. setting:: IEVV_SLUGIFY_CHARACTER_REPLACE_MAP

IEVV_SLUGIFY_CHARACTER_REPLACE_MAP
==================================
Custom character replacement map for the ``ievv_slugify`` function



.. setting:: IEVV_COLORIZE_USE_COLORS

IEVV_COLORIZE_USE_COLORS
========================
Colorize output from :func:`ievv_opensource.utils.ievv_colorize.colorize`? Defaults
to ``True``.
