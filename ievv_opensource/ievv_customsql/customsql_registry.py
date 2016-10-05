# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import inspect
import os
from collections import OrderedDict

from django import template
from django.db import connection
from ievv_opensource.utils.singleton import Singleton


class AbstractCustomSql(object):
    """
    Defines custom SQL that can be executed by the ``ievv_customsql`` framework.

    You typically override :meth:`.initialize` and use :meth:`.execute_sql` to add
    triggers and functions, and override :meth:`.recreate_data` to rebuild the data
    maintained by the triggers, but many other use-cases are also possible.
    """
    def __init__(self, appname=None):
        """
        Args:
            appname: Not required - it is added automatically by :class:`.Registry`, and
                used by :meth:`.__str__`` for easier debugging / prettier output.
        """
        self.appname = appname

    def execute_sql(self, sql):
        """
        Execute the provided SQL.

        Args:
            sql (str): String of SQL.
        """
        cursor = connection.cursor()
        cursor.execute(sql)

    def get_sql_from_file(self, path):
        """
        Get SQL from a file as a string.

        Args:
            path (str): A path relative to a directory named the same as the module
                where this class is located without the filename extension.

                So if the file with this class is in ``path/to/customsql.py``,
                path will be relative to ``path/to/customsql/``.
        """
        this_file_path = inspect.getfile(self.__class__)
        sqldirectory = os.path.join(
            os.path.dirname(inspect.getfile(self.__class__)),
            os.path.splitext(this_file_path)[0])
        full_path = os.path.join(sqldirectory, path)
        return open(full_path, 'rb').read().decode('utf-8')

    def execute_sql_from_file(self, path):
        """
        Execute SQL from the provided file.

        Args:
            path: See :meth:`.get_sql_from_file`.
        """
        self.execute_sql(self.get_sql_from_file(path))

    def execute_sql_from_files(self, paths):
        """
        Shortcut for calling :meth:`.execute_sql_from_file`
        with multiple files.

        Calls :meth:`.execute_sql_from_file` once for each file
        in ``paths``.

        Args:
            paths (list): A list of paths. See :meth:`.get_sql_from_file`
                for the format of each path.
        """
        for path in paths:
            self.execute_sql_from_file(path=path)

    def execute_sql_from_template_file(self, path, context_data=None):
        """
        Execute SQL from the provided Django template file.

        The SQL is retrieved from the file, then processed as a Django
        template with the provided ``context_data``, and the result
        is executed using :meth:`.execute_sql`.

        Args:
            path: See :meth:`.get_sql_from_file`.
            context_data (dict): Template context data. Can be ``None``.
        """
        template_sql = self.get_sql_from_file(path)
        context_data = context_data or {}
        djangotemplate = template.Template(template_sql)
        sql = djangotemplate.render(template.Context(context_data))
        self.execute_sql(sql)

    def execute_sql_from_template_files(self, paths, context_data=None):
        """
        Shortcut for calling :meth:`.execute_sql_from_template_file`
        with multiple files.

        Calls :meth:`.execute_sql_from_template_file` once for each file
        in ``paths``.

        Args:
            paths (list): A list of paths. See :meth:`.get_sql_from_file`
                for the format of each path.
            context_data (dict): Forwarded to :meth:`.execute_sql_from_template_file`.
        """
        for path in paths:
            self.execute_sql_from_template_file(path=path, context_data=context_data)

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

        Can not be used unless :meth:`.initialize` has already be run (at some point).
        This restriction is here to make it possible to create SQL functions
        in :meth:`.initialize` that this method uses to recreate the data. Without this
        restriction, code-reuse between :meth:`.initialize` and this function would be
        very difficult.
        """
        pass

    def run(self):
        """
        Run both :meth:`.initialize` and :meth:`.recreate_data`.
        """
        self.initialize()
        self.recreate_data()

    def __str__(self):
        return '{} in {}'.format(self.__class__.__name__, self.appname)


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

        See ``ievv_opensource/demo/customsql/apps.py`` for a complete demo.
    """

    def __init__(self):
        super(Registry, self).__init__()
        self._customsql_classes = []
        self._customsql_classes_by_appname_map = OrderedDict()

    def add(self, appname, customsql_class):
        """
        Add the given ``customsql_class`` to the registry.

        Parameters:
            appname: The django appname where the ``customsql_class`` belongs.
            customsql_class: A subclass of :class:`.AbstractCustomSql`.
        """
        if customsql_class in self._customsql_classes:
            raise ValueError('{}.{} is already in the custom SQL registry.'.format(
                customsql_class.__module__, customsql_class.__name__))
        self._customsql_classes.append(customsql_class)
        if appname not in self._customsql_classes_by_appname_map:
            self._customsql_classes_by_appname_map[appname] = []
        self._customsql_classes_by_appname_map[appname].append(customsql_class)

    def remove(self, appname, customsql_class):
        self._customsql_classes.remove(customsql_class)
        self._customsql_classes_by_appname_map[appname].remove(customsql_class)
        if len(self._customsql_classes_by_appname_map[appname]) == 0:
            del self._customsql_classes_by_appname_map[appname]

    def __contains__(self, customsql_class):
        """
        Returns ``True`` if the provided customsql_class is in the registry.

        Parameters:
            customsql_class: A subclass of :class:`.AbstractCustomSql`.
        """
        return customsql_class in self._customsql_classes

    def __iter__(self):
        """
        Iterate over all :class:`.AbstractCustomSql` subclasses registered
        in the registry. The yielded values are objects of the
        classes initialized with no arguments.
        """
        for appname in self.iter_appnames():
            for customsql in self.iter_customsql_in_app(appname):
                yield customsql

    def iter_appnames(self):
        """
        Returns an iterator over all the appnames in the registry.
        Each item in the iterator is an appname (a string).
        """
        return iter(self._customsql_classes_by_appname_map.keys())

    def iter_customsql_in_app(self, appname):
        """
        Iterate over all :class:`.AbstractCustomSql` subclasses registered
        in the provided appname. The yielded values are objects of the
        classes initialized with no arguments.
        """
        for customsql_class in self._customsql_classes_by_appname_map[appname]:
            yield customsql_class(appname)

    def run_all_in_app(self, appname):
        """
        Loops through all the :class:`.AbstractCustomSql` classes registered in the registry
        with the provided ``appname``, and call :meth:`.AbstractCustomSql.run` for each of them.
        """
        for customsql in self.iter_customsql_in_app(appname):
            customsql.run()

    def run_all(self):
        """
        Loops through all the :class:`.AbstractCustomSql` classes in the registry, and call
        :meth:`.AbstractCustomSql.run` for each of them.
        """
        for customsql in self:
            customsql.run()


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
