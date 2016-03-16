import elasticsearch_dsl
from django import test
from django_cradmin import datetimeutils
from model_mommy import mommy

from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.ievv_elasticsearch2.tests.ievv_elasticsearch2_testapp.models import ModelmapperModel, \
    ModelMapperChildModel, ModelMapperForeignKeyModel


class AutomappedDocType(ievv_elasticsearch2.DocType):
    modelmapper = ievv_elasticsearch2.Modelmapper(ModelmapperModel, automap_fields=True)
    char = elasticsearch_dsl.String()
    text = elasticsearch_dsl.String()
    smallint = elasticsearch_dsl.Short()
    int = elasticsearch_dsl.Integer()
    bigint = elasticsearch_dsl.Long()
    float = elasticsearch_dsl.Double()
    boolean = elasticsearch_dsl.Boolean()
    date = elasticsearch_dsl.Date()
    datetime = elasticsearch_dsl.Date()
    parent_id = elasticsearch_dsl.Long()

    class Meta:
        index = 'main'


class WithForeignKeyObjectModelmapper(ievv_elasticsearch2.Modelmapper):
    parent = ievv_elasticsearch2.ForeignKeyObjectMapping(
        modelmapper=ievv_elasticsearch2.Modelmapper(model_class=ModelMapperForeignKeyModel,
                                                    automap_fields=True))


class WithForeignKeyObjectDocType(ievv_elasticsearch2.DocType):
    modelmapper = WithForeignKeyObjectModelmapper(ModelmapperModel)
    parent = elasticsearch_dsl.Object()

    class Meta:
        index = 'main'


class WithForeignKeyPrefixModelmapper(ievv_elasticsearch2.Modelmapper):
    parent = ievv_elasticsearch2.ForeignKeyPrefixMapping(
        modelmapper=ievv_elasticsearch2.Modelmapper(model_class=ModelMapperForeignKeyModel,
                                                    automap_fields=True))


class WithForeignKeyPrefixDocType(ievv_elasticsearch2.DocType):
    modelmapper = WithForeignKeyPrefixModelmapper(ModelmapperModel)
    parent__id = elasticsearch_dsl.Long()
    parent__name = elasticsearch_dsl.String()

    class Meta:
        index = 'main'


class TestModelmapperValidateFieldMapping(test.TestCase):
    def test_modelfield_field_does_not_exist(self):
        class MyModelmapper(ievv_elasticsearch2.Modelmapper):
            not_on_model = ievv_elasticsearch2.StringMapping('not_on_model')

        with self.assertRaises(ievv_elasticsearch2.ModelFieldDoesNotExist):
            class MyDocType(ievv_elasticsearch2.DocType):
                modelmapper = MyModelmapper(ModelmapperModel)
                not_on_model = elasticsearch_dsl.String()

                class Meta:
                    index = 'main'

    def test_doctypefield_does_not_exist(self):
        class MyModelmapper(ievv_elasticsearch2.Modelmapper):
            text = ievv_elasticsearch2.StringMapping('text')

        with self.assertRaises(ievv_elasticsearch2.DoctypeFieldDoesNotExist):
            class MyDocType(ievv_elasticsearch2.DocType):
                modelmapper = MyModelmapper(ModelmapperModel)

                class Meta:
                    index = 'main'


class TestModelmapperAutomap(test.TestCase):
    # def setUp(self):
    #     self.es = connections.get_connection()
    #     self.es.indices.delete(index='_all')
    #     self.es.indices.flush(index='_all')

    def test_automap_charfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('char'),
                              ievv_elasticsearch2.StringMapping)

    def test_automap_textfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('text'),
                              ievv_elasticsearch2.StringMapping)

    def test_automap_integerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('int'),
                              ievv_elasticsearch2.IntegerMapping)

    def test_automap_bigintegerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('bigint'),
                              ievv_elasticsearch2.BigIntegerMapping)

    def test_automap_smallintegerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('smallint'),
                              ievv_elasticsearch2.SmallIntegerMapping)

    def test_automap_booleanfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('boolean'),
                              ievv_elasticsearch2.BooleanMapping)

    def test_automap_floatfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('float'),
                              ievv_elasticsearch2.DoubleMapping)

    def test_automap_datefield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('date'),
                              ievv_elasticsearch2.DateMapping)

    def test_automap_datetimefield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('datetime'),
                              ievv_elasticsearch2.DateTimeMapping)


class TestModelmapperToDict(test.TestCase):
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
