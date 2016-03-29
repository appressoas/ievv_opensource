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



*************
Writing tests
*************
TODO - helpers and full example


************************
Define and use a DocType
************************

Simple example - define a doctype in the "main" index with
name and age fields::

    import elasticsearch_dsl
    from ievv_opensource import ievv_elasticsearch2

    class MyDocType(ievv_elasticsearch2.DocType):
        name = elasticsearch_dsl.String()
        age = elasticsearch_dsl.Integer()

        class Meta:
            index = 'main'

Add some data to ``MyDocType``::

    document = MyDocType(name="Jane Doe", age=26)
    document.save()

    document = MyDocType(name="John Doe", age=33)
    document.save()

    document = MyDocType(name="Peter", age=21)
    document.save()

Search ``MyDocType``::

    result = MyDocType.objects.query('match', name='Doe').execute()
    print(result)


Re-usable search
================

The search above is fine, but what if we want to create a re-usable query
for the name field?. We simply override the ``objects``-attribute with
our own :class:`ievv_opensource.ievv_elasticsearch2.search.Search` object::

    import elasticsearch_dsl
    from ievv_opensource import ievv_elasticsearch2

    class MyDocTypeSearch(ievv_elasticsearch2.Search):
        def query_name(self, name):
            return self.query('match', name=name)


    class MyDocType(ievv_elasticsearch2.DocType):
        objects = MyDocTypeSearch()
        name = elasticsearch_dsl.String()

        class Meta:
            index = 'main'

Now we can search by name using the new ``query_name``-method::

    result = MyDocType.objects.query_name(name='Doe').execute()
    print(result)

We can other search-objects to our DocType than just the ``objects`` attribute::

    import elasticsearch_dsl
    from ievv_opensource import ievv_elasticsearch2

    class MyDocTypeSearch(ievv_elasticsearch2.Search):
        def query_name(self, name):
            return self.query('match', name=name)

    class FancyMyDocTypeSearch(ievv_elasticsearch2.Search):
        def query_all(self, text):
            return self.query(
                ievv_elasticsearch2.Q('match', name=text) |
                ievv_elasticsearch2.Q('match', description=text))

    class MyDocType(ievv_elasticsearch2.DocType):
        objects = MyDocTypeSearch()
        fancysearch = FancyMyDocTypeSearch()
        name = elasticsearch_dsl.String()
        description = elasticsearch_dsl.String()

        class Meta:
            index = 'main'

    result = MyDocType.objects.query_name(name='Doe').execute()
    print(result)
    result = MyDocType.fancysearch.query_all(name='Doe').execute()
    print(result)

Multiple search-objects is mostly useful for the same reasons as multiple QuerySets
with Django models - they are useful to segment your queries, or to group queries.


.. currentmodule:: ievv_opensource.ievv_elasticsearch2.doctype

.. autoclass:: DocType



DocTypeRegistry
===============

.. currentmodule:: ievv_opensource.ievv_elasticsearch2.doctype

.. autoclass:: DocTypeRegistry


Abstract DocType
================
A DocType can be abstract. In simple terms, this means that



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
