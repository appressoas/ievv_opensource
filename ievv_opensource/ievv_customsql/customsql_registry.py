# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import connection

from ievv_opensource.utils.singleton import Singleton


class AbstractCustomSql(object):
    """
    Defines custom SQL that can be executed by the ``ievv_customsql`` framework.

    You typically override :meth:`.initialize` and use :meth:`.execute_sql` to add
    triggers and functions, and override :meth:`.recreate_data` to rebuild the data
    maintained by the triggers, but many other use-cases are also possible.
    """
    def execute_sql(self, sql):
        cursor = connection.cursor()
        cursor.execute(sql)

    def initialize(self):
        """
        Code to initialize the custom SQL.

        You should create triggers, functions, columns, indexes, etc. in this
        method, using :meth:`.execute_sql`, or using plain Django code.

        Make sure to write everything in a manner that updates or creates
        everything in a self-contained manner. This method is called both
        for the first initialization, and to update code after updates/changes.

        Must be overridden in subclasses.
        """
        raise NotImplementedError()

    def recreate_data(self):
        """
        Recreate all data that any triggers created in :meth:`.initialize`
        would normally keep in sync automatically.
        """
        pass

    def run(self):
        """
        Run both :meth:`.initialize` and :meth:`.recreate_data`.
        """
        self.initialize()
        self.recreate_data()


class Registry(Singleton):
    """
    Registry of :class:`.AbstractCustomSql` objects.

    Examples:

        First, define a subclass of :class:`.AbstractCustomSql`.

        Register the custom SQL class with the registry via an AppConfig for your
        Django app::

            from django.apps import AppConfig
            from ievv_opensource.ievv_customsql import customsql_registry

            from myapp import customsql


            class MyAppConfig(AppConfig):
                name = 'myapp'

                def ready(self):
                    customsql_registry.Registry.get_instance().add(customsql.MyCustomSql)
    """

    def __init__(self):
        super(Registry, self).__init__()
        self._customsql_classes = []

    def add(self, customsql_class):
        """
        Add the given ``customsql_class`` to the registry.

        Parameters:
            customsql_class: A subclass of :class:`.AbstractCustomSql`.
        """
        if customsql_class in self._customsql_classes:
            raise ValueError('{}.{} is already in the custom SQL registry.'.format(
                customsql_class.__module__, customsql_class.__name__))
        self._customsql_classes.append(customsql_class)

    def __contains__(self, customsql_class):
        """
        Check if the provided customsql_class is in the registry.

        Parameters:
            customsql_class: A subclass of :class:`.AbstractCustomSql`.
        """
        return customsql_class in self._customsql_classes

    def run_all(self):
        """
        Loops through all the :class:`.CustomSql` classes in the registry, and call
        :meth:`.CustomSql.run` for each of them.
        """
        for customsql_class in self._customsql_classes:
            customsql_class().run()


class MockableRegistry(Registry):
    """
    A non-singleton version of :class:`.Registry`. For tests.

    Typical usage in a test::

        from ievv_opensource.ievv_customsql import customsql_registry

        class MockCustomSql(customsql_registry.AbstractCustomSql):
            # ...

        mockregistry = customsql_registry.MockableRegistry()
        mockregistry.add(MockCustomSql())

        with mock.patch('ievv_opensource.ievv_customsql.customsql_registry.Registry.get_instance',
                        lambda: mockregistry):
            pass  # ... your code here ...
    """

    def __init__(self):
        self._instance = None  # Ensure the singleton-check is not triggered
        super(MockableRegistry, self).__init__()
