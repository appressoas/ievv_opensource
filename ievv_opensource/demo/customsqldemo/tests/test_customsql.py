# -*- coding: utf-8 -*-
from django import test
from model_bakery import baker

from ievv_opensource.demo.customsqldemo.customsql import PersonCustomSql
from ievv_opensource.demo.customsqldemo.models import Person


class TestPersonCustomSql(test.TestCase):
    def test_add_person_and_search(self):
        PersonCustomSql().initialize()
        jack = baker.make('customsqldemo.Person', name='Jack The Man', description='Also called john by some.')
        baker.make('customsqldemo.Person', name='NoMatch Man')
        john = baker.make('customsqldemo.Person', name='John Peterson', description='Hello world')

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

    def test_recreate_data(self):
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

        # Add data before we setup the triggers that maintains the search index
        jack = baker.make('customsqldemo.Person', name='Jack The Man', description='Also called john by some.')
        baker.make('customsqldemo.Person', name='NoMatch Man')
        john = baker.make('customsqldemo.Person', name='John Peterson', description='Hello world')

        # Create the search_verctor column, trigger - but we do this after we added
        # the data, so nothing is added to the search index!
        PersonCustomSql().initialize()
        self.assertEqual(0, queryset.count())

        # So we have to populate the search index - it now works!
        PersonCustomSql().recreate_data()
        self.assertEqual([john, jack], list(queryset))
