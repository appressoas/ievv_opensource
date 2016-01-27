############################################################
`ievv_elasticsearch` --- Thin wrapper around pyelasticsearch
############################################################

The ``ievv_elasticsearch`` module is designed to just make it
a small bit easier to work with elasticsearch in Django than to just
use pyelasticsearch_.


********
Features
********
- Makes ``pyelasticsearch`` easy to use in Django.
- Very thin wrapper around ``pyelasticsearch``. This means that you use
  the elasticsearch REST API almost directly with just some pythonic
  glue.
- Automatic indexing of data store data is decoupled from the search/get API.
- Automatic indexing of data store data works with any data store.
  Our examples use Django ORM, but you can just as easily use a NOSQL
  database like MongoDB or an XML database. The only difference is the
  code you provide to convert your data store data into ElasticSearch
  JSON compatible data structures.
- Small Django/python helpers that enhances the ``pyelasticsearch`` API.
- Shortcuts and solutions that makes unit testing easy.


Why not use Haystack?
=====================
Haystack_ is an awesome library for full text document search in a
search engine independent manner. But if you want to make full
use of ElasticSearch as more than just a document search index,
and use it for analytics, document caching and a general purpose
nosql data store, haystack just adds an extra layer of complexity
that you have to work around. This is, of course, use-case dependent,
and many use cases will probably be better served by a combination of
``ievv_elasticsearch`` and Haystack_.

.. note:: If considering combining Haystack_ with ``ievv_elasticsearch``, you
    should know that ``ievv_elasticsearch`` has loose coupling between
    index definition and querying. Indexe definitions in ``ievv_elasticsearch`` are
    only used to make it easy to sync the backend data store into an elasticseach
    index. If you define the search indexes in haystack, you can still use
    the :mod:`ievv_opensource.ievv_elasticsearch.search` API, you just ignore
    :mod:`ievv_opensource.ievv_elasticsearch.autoindex`.



***************
Getting started
***************
You only need the following to get started:

- ElasticSearch server.
- Configure ``IEVV_ELASTICSEARCH_URL`` with the URL of the server.

Then you can start using the :class:`ievv_opensource.ievv_elasticsearch.search.Connection`
API.


Setup for unit-testing and development
======================================
First, copy ``not_for_deploy/elasticsearch.develop.yml`` and ``not_for_deploy/elasticsearch.unittest.yml``
into your own project.

In your **test settings**, add::

    IEVV_ELASTICSEARCH_TESTURL = 'http://localhost:9251'
    IEVV_ELASTICSEARCH_TESTMODE = True
    IEVV_ELASTICSEARCH_AUTOREFRESH_AFTER_INDEXING = True

In your **develop settings**, add::

    IEVV_ELASTICSEARCH_URL = 'http://localhost:9252'

When this is configured, you can run elasticsearch with :doc:`ievvtask_devrun` if
you add the following to :setting:`IEVVTASKS_DEVRUN_RUNNABLES`::

    IEVVTASKS_DEVRUN_RUNNABLES = {
        'default': ievvdevrun.config.RunnableThreadList(
            # ...
            ievvdevrun.runnables.elasticsearch.RunnableThread(configpath='not_for_deploy/elasticsearch.unittest.yml'),
            ievvdevrun.runnables.elasticsearch.RunnableThread(configpath='not_for_deploy/elasticsearch.develop.yml'),
        ),
    ]

(the paths assumes you put the configfiles in the ``not_for_deploy/`` directory in your project).


***************************************
Automatically update the search indexes
***************************************
Unless you use ElasticSearch as the primary data source, you will most
likely want an easy method of:
1. Update the search index when data in the data store changes.
2. Rebuild the search index from the data in the data store.

This is solved by:

#. Define a :class:`ievv_opensource.ievv_elasticsearch.autoindex.AbstractIndex`. The ``ievv_elasticsearch``
   convention is to put search indexes in ``yourapp.elasticsearch_autoindexes``.
#. Register the index class in :class:`ievv_opensource.ievv_elasticsearch.autoindex.Registry`.
#. Optionally override :meth:`ievv_opensource.ievv_elasticsearch.autoindex.AbstractIndex.register_index_update_triggers`.
   and register triggers that react to data store changes and trigger re-indexing.


**********
search API
**********

.. currentmodule:: ievv_opensource.ievv_elasticsearch.search

.. autosummary::
   :nosignatures:

   ievv_opensource.ievv_elasticsearch.search.Connection
   ievv_opensource.ievv_elasticsearch.search.SearchResultWrapper
   ievv_opensource.ievv_elasticsearch.search.SearchResultItem
   ievv_opensource.ievv_elasticsearch.search.Paginator

.. automodule:: ievv_opensource.ievv_elasticsearch.search
    :members:


*************
autoindex API
*************

.. currentmodule:: ievv_opensource.ievv_elasticsearch.autoindex

.. autosummary::
   :nosignatures:

   ievv_opensource.ievv_elasticsearch.autoindex.AbstractIndex
   ievv_opensource.ievv_elasticsearch.autoindex.AbstractDocument
   ievv_opensource.ievv_elasticsearch.autoindex.AbstractDictDocument
   ievv_opensource.ievv_elasticsearch.autoindex.Registry
   ievv_opensource.ievv_elasticsearch.autoindex.MockableRegistry

.. automodule:: ievv_opensource.ievv_elasticsearch.autoindex
    :members:


**************
jsondecode API
**************

.. currentmodule:: ievv_opensource.ievv_elasticsearch.jsondecode

.. automodule:: ievv_opensource.ievv_elasticsearch.jsondecode
    :members:


***************
viewhelpers API
***************

.. currentmodule:: ievv_opensource.ievv_elasticsearch.viewhelpers.searchview

.. autosummary::
   :nosignatures:

   ievv_opensource.ievv_elasticsearch.viewhelpers.searchview.ViewMixin
   ievv_opensource.ievv_elasticsearch.viewhelpers.searchview.View
   ievv_opensource.ievv_elasticsearch.viewhelpers.searchview.SortMixin
   ievv_opensource.ievv_elasticsearch.viewhelpers.searchview.SearchMixin

.. automodule:: ievv_opensource.ievv_elasticsearch.viewhelpers.searchview
    :members:


.. _pyelasticsearch: https://pyelasticsearch.readthedocs.org
.. _Haystack: https://pyelasticsearch.readthedocs.org
