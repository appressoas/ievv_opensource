###################################################################
`ievv_customsql` --- Framework for adding custom SQL to Django apps
###################################################################

The intention of this module is to make it easier to add and update
custom SQL in a Django app. We do this by providing a registry
of all custom SQL, and a management command to add and update
custom SQL and any refresh data that is maitained by triggers.


*************
Configuration
*************
Add the following to your ``INSTALLED_APPS``-setting::

    'ievv_opensource.ievv_customsql'


**************************
Add custom SQL to your app
**************************


Create the class containing your custom SQL
===========================================

First you need to create a subclass of
:class:`~ievv_opensource.ievv_customsql.customsql_registry.AbstractCustomSql`.

Lets say you have a Person model with name and description. You want to maintain
a fulltext search vector to efficiently search the person model. You would then
create a subclass of AbstractCustomSql that looks something like this::

    from ievv_opensource.ievv_customsql import customsql_registry


    class PersonCustomSql(customsql_registry.AbstractCustomSql):
        def initialize(self):
            self.execute_sql("""

                -- Add search_vector column to the Person model
                ALTER TABLE myapp_person DROP COLUMN IF EXISTS search_vector;
                ALTER TABLE myapp_person ADD COLUMN search_vector tsvector;

                -- Function used to create the search_vector value both in the trigger,
                -- and in the UPDATE statement (in recreate_data()).
                CREATE OR REPLACE FUNCTION myapp_person_get_search_vector_value(param_table myapp_person)
                RETURNS tsvector AS $$
                BEGIN
                    RETURN setweight(to_tsvector(param_table.name), 'A') ||
                        setweight(to_tsvector(param_table.description), 'C');
                END
                $$ LANGUAGE plpgsql;

                -- Trigger function called on insert or update to keep the search_vector column
                -- in sync.
                CREATE OR REPLACE FUNCTION myapp_person_set_search_vector() RETURNS trigger AS $$
                BEGIN
                    NEW.search_vector := myapp_person_get_search_vector_value(NEW);
                  return NEW;
                END
                $$ LANGUAGE plpgsql;

                DROP TRIGGER IF EXISTS myapp_person_set_search_vector_trigger ON myapp_person;
                CREATE TRIGGER myapp_person_set_search_vector_trigger BEFORE INSERT OR UPDATE
                    ON myapp_person FOR EACH ROW
                    EXECUTE PROCEDURE myapp_person_set_search_vector();
            """)

        def recreate_data(self):
            self.execute_sql("""
                UPDATE myapp_person SET
                    search_vector = myapp_person_get_search_vector_value(myapp_person);
            """)

You can put this code anywhere in your app, but the recommended location is to put it in
a file named ``customsql.py`` in the root of your app.


Add your custom SQL to the registry
===================================

Next, you need to register your PersonCustomSql class in the registry. Create
an AppConfig for your app with the following code::

    from django.apps import AppConfig

    from ievv_opensource.ievv_customsql import customsql_registry
    from myproject.myapp.customsqldemo.customsql import PersonCustomSql


    class CustomSqlDemoAppConfig(AppConfig):
        name = 'myproject.myapp'
        verbose_name = "My APP"

        def ready(self):
            registry = customsql_registry.Registry.get_instance()
            registry.add('myapp', PersonCustomSql)


Using your custom SQL
=====================
During development and as part of production releases, you use the ``ievvtasks_customsql``
command to update your custom SQL. Run the following to execute both:

- :meth:`~ievv_opensource.ievv_customsql.customsql_registry.AbstractCustomSql.initialize`
- :meth:`~ievv_opensource.ievv_customsql.customsql_registry.AbstractCustomSql.recreate_data`

for all the custom SQL classes in the registry::

    $ python manage.py ievvtasks_customsql -i -r

Since this is an ievvtasks command, you can also run it as::

    $ ievv customsql -i -r


Writing tests using your custom SQL
===================================
.. currentmodule:: ievv_opensource.ievv_customsql.customsql_registry

The custom SQL is not added automatically, so you need to use it explicitly in your tests.
You have three choices:

1. Call ``PersonCustomSql().initialize()`` in your setUp() method,
   or in your test method(s). You will probably also want to call ``PersonCustomSql().recreate_data()``
   when required. This is **normally the recommented method**, since it provides the largest amount
   of control.
   See :meth:`.AbstractCustomSql.initialize` and :meth:`.AbstractCustomSql.recreate_data` for more info.
2. Call ``ievv_customsql.Registry.get_instance().run_all_in_app('myapp')``. This may be useful
   to test views and other code that require all the custom SQL in your app.
   See :meth:`.Registry.run_all_in_app` for more info.
3. Call ``ievv_customsql.Registry.get_instance().run_all()``. This is **not recommended** because
   it runs SQL from ALL apps in ``INSTALLED_APPS``. See
   See :meth:`.Registry.run_all` for more info.

Example of using option (1) to create a TestCase::

    class TestPersonCustomSql(test.TestCase):
        def test_add_person_and_search(self):
            PersonCustomSql().initialize()
            jack = mommy.make('myapp.Person', name='Jack The Man', description='Also called john by some.')
            mommy.make('myapp.Person', name='NoMatch Man')
            john = mommy.make('myapp.Person', name='John Peterson', description='Hello world')

            tsquery = 'john'
            queryset = Person.objects.extra(
                select={
                    'rank': 'ts_rank_cd(search_vector, to_tsquery(%s))',
                },
                select_params=[tsquery],
                where=['search_vector @@ to_tsquery(%s)'],
                params=[tsquery],
                order_by=['-rank']
            )
            self.assertEqual([john, jack], list(queryset))


Demo
====
See ``ievv_opensource/demo/customsqldemo/`` for a full demo of everything explained above.


***
API
***

.. currentmodule:: ievv_opensource.ievv_customsql.customsql_registry


AbstractCustomSql
=================
.. autoclass:: ievv_opensource.ievv_customsql.customsql_registry.AbstractCustomSql


Registry
========
.. autoclass:: ievv_opensource.ievv_customsql.customsql_registry.Registry


MockableRegistry
================
.. autoclass:: ievv_opensource.ievv_customsql.customsql_registry.MockableRegistry
