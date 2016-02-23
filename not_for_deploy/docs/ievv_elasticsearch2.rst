###############################################################
`ievv_elasticsearch2` --- Makes working with ElasticSearch easy
###############################################################
Extends `elasticsearch-py`_ and `elasticsearch-dsl`_ with some very
useful utilities that makes it easier to use ElasticSearch with
Django.


*******
Install
*******
Add ``"ievv_opensource.ievv_elasticsearch2.apps.IevvEsAppConfig"`` to ``INSTALLED_APPS``.

*****
Goals
*****
The goal of ``ievv_elasticsearch2`` is to extend elasticsearch-dsl
with::

- Django settings based configuration.
- Configuration that makes it easy to write tests.
- Configuration that makes it easy to disable certain indexing
  operations.
- Common structure for handling index updates, even for complex
  cases where performance is really important. This includes a
  structure that makes offloading heavy indexing operations to Celery
  easy to do and easy to maintain.
- Base views and mixins that simplify making ElasticSearch views.
- Base views and mixins that simplify using ElasticSearch with Django-CRadmin.
- ... in short - DRY with elasticsearch-dsl in Django projects ...


**********
Search API
**********

Usage example::

    import ievv_elasticsearch2

    search = ievv_elasticsearch2.Search()\
        .query('match', title='python')
    print(search.ievv_execute())






.. _`elasticsearch-dsl`: http://elasticsearch-dsl.readthedocs.org/
.. _`elasticsearch-py`: http://elasticsearch-py.readthedocs.org/
