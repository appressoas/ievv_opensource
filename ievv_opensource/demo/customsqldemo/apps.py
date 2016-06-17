# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.apps import AppConfig

from ievv_opensource.demo.customsqldemo.customsql import PersonCustomSql
from ievv_opensource.ievv_customsql import customsql_registry


class CustomSqlDemoAppConfig(AppConfig):
    name = 'ievv_opensource.demo.customsqldemo'
    verbose_name = "IEVV CustomSQL demo"

    def ready(self):
        registry = customsql_registry.Registry.get_instance()
        registry.add('customsqldemo', PersonCustomSql)
