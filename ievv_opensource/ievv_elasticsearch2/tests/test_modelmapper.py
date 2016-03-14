from pprint import pprint

import elasticsearch_dsl
from django import test
from django_cradmin import datetimeutils
from model_mommy import mommy

from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.ievv_elasticsearch2.tests.ievv_elasticsearch2_testapp.models import ModelmapperModel, \
    ModelMapperChildModel, ModelMapperForeignKeyModel


class AutomappedDocType(ievv_elasticsearch2.DocType):
    modelmapper = ievv_elasticsearch2.Modelmapper(ModelmapperModel, automap_fields=True)

    class Meta:
        index = 'main'


class WithForeignKeyObjectModelmapper(ievv_elasticsearch2.Modelmapper):
    parent = ievv_elasticsearch2.ForeignKeyObjectMapping(
        modelmapper=ievv_elasticsearch2.Modelmapper(model_class=ModelMapperForeignKeyModel,
                                                    automap_fields=True))


class WithForeignKeyObjectDocType(ievv_elasticsearch2.DocType):
    modelmapper = WithForeignKeyObjectModelmapper(ModelmapperModel)

    class Meta:
        index = 'main'


class WithForeignKeyPrefixModelmapper(ievv_elasticsearch2.Modelmapper):
    parent = ievv_elasticsearch2.ForeignKeyPrefixMapping(
        modelmapper=ievv_elasticsearch2.Modelmapper(model_class=ModelMapperForeignKeyModel,
                                                    automap_fields=True))


class WithForeignKeyPrefixDocType(ievv_elasticsearch2.DocType):
    modelmapper = WithForeignKeyPrefixModelmapper(ModelmapperModel)

    class Meta:
        index = 'main'


class TestModelmapper(test.TestCase):
    # def setUp(self):
    #     self.es = connections.get_connection()
    #     self.es.indices.delete(index='_all')
    #     self.es.indices.flush(index='_all')

    def test_automap_charfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['char'],
                              ievv_elasticsearch2.StringMapping)

    def test_automap_textfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['text'],
                              ievv_elasticsearch2.StringMapping)

    def test_automap_integerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['int'],
                              ievv_elasticsearch2.IntegerMapping)

    def test_automap_bigintegerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['bigint'],
                              ievv_elasticsearch2.BigIntegerMapping)

    def test_automap_smallintegerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['smallint'],
                              ievv_elasticsearch2.SmallIntegerMapping)

    def test_automap_booleanfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['boolean'],
                              ievv_elasticsearch2.BooleanMapping)

    def test_automap_floatfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['float'],
                              ievv_elasticsearch2.DoubleMapping)

    def test_automap_datefield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['date'],
                              ievv_elasticsearch2.DateMapping)

    def test_automap_datetimefield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper['datetime'],
                              ievv_elasticsearch2.DateTimeMapping)

    def test_to_dict_simple_field_types(self):
        parent = mommy.make(ModelMapperForeignKeyModel)
        testdatetime = datetimeutils.default_timezone_datetime(2015, 12, 24, 18, 30)
        testobject = mommy.make(ModelmapperModel,
                                char='Char',
                                text='Text',
                                smallint=5,
                                int=10,
                                bigint=20,
                                float=0,
                                boolean=True,
                                date=testdatetime.date(),
                                datetime=testdatetime,
                                parent=parent)
        self.assertEqual(
            {'char': 'Char',
             'text': 'Text',
             'smallint': 5,
             'int': 10,
             'bigint': 20,
             'float': 0,
             'boolean': True,
             'date': testdatetime.date(),
             'datetime': testdatetime,
             'parent_id': parent.id},
            AutomappedDocType.modelmapper.to_dict(testobject))

    def test_to_dict_foreign_key_object_mapping(self):
        testobject = mommy.make(ModelmapperModel, parent__name='Test name')
        self.assertEqual(
            {'parent': {'name': 'Test name'}},
            WithForeignKeyObjectDocType.modelmapper.to_dict(testobject))

    def test_to_dict_foreign_key_prefix_mapping(self):
        testobject = mommy.make(ModelmapperModel, parent__name='Test name')
        self.assertEqual(
            {'parent__name': 'Test name'},
            WithForeignKeyPrefixDocType.modelmapper.to_dict(testobject))
