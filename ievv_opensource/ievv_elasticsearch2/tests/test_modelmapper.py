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
    xint = elasticsearch_dsl.Integer()
    bigint = elasticsearch_dsl.Long()
    xfloat = elasticsearch_dsl.Double()
    xboolean = elasticsearch_dsl.Boolean()
    date = elasticsearch_dsl.Date()
    datetime = elasticsearch_dsl.Date()
    parent = elasticsearch_dsl.Long()

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


class OneToManyNestedMappingModelmapper(ievv_elasticsearch2.Modelmapper):
    children = ievv_elasticsearch2.OneToManyNestedMapping(
        modelmapper=ievv_elasticsearch2.Modelmapper(model_class=ModelMapperChildModel,
                                                    automap_fields=True,
                                                    exclude=['parent']))


class OneToManyNestedMappingDocType(ievv_elasticsearch2.DocType):
    modelmapper = OneToManyNestedMappingModelmapper(ModelmapperModel)
    children = elasticsearch_dsl.Nested()

    class Meta:
        index = 'main'


class OneToManyIdArrayMappingModelmapper(ievv_elasticsearch2.Modelmapper):
    children = ievv_elasticsearch2.OneToManyIdArrayMapping()


class OneToManyIdArrayMappingDocType(ievv_elasticsearch2.DocType):
    modelmapper = OneToManyIdArrayMappingModelmapper(ModelmapperModel)
    children = elasticsearch_dsl.Nested()

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
    def test_automap_charfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('char'),
                              ievv_elasticsearch2.StringMapping)

    def test_automap_textfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('text'),
                              ievv_elasticsearch2.StringMapping)

    def test_automap_integerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('xint'),
                              ievv_elasticsearch2.IntegerMapping)

    def test_automap_bigintegerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('bigint'),
                              ievv_elasticsearch2.BigIntegerMapping)

    def test_automap_smallintegerfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('smallint'),
                              ievv_elasticsearch2.SmallIntegerMapping)

    def test_automap_booleanfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('xboolean'),
                              ievv_elasticsearch2.BooleanMapping)

    def test_automap_floatfield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('xfloat'),
                              ievv_elasticsearch2.DoubleMapping)

    def test_automap_datefield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('date'),
                              ievv_elasticsearch2.DateMapping)

    def test_automap_datetimefield(self):
        self.assertIsInstance(AutomappedDocType.modelmapper.get_mappingfield_by_modelfieldname('datetime'),
                              ievv_elasticsearch2.DateTimeMapping)

    def test_automap_no_pk_by_default(self):
        modelmapper = ievv_elasticsearch2.Modelmapper(model_class=ModelMapperForeignKeyModel,
                                                      automap_fields=True)
        self.assertEqual({'name'}, set(modelmapper.mappingfields.keys()))

    def test_automap_id_field(self):
        modelmapper = ievv_elasticsearch2.Modelmapper(model_class=ModelMapperForeignKeyModel,
                                                      automap_fields=True, automap_id_field=True)
        self.assertEqual({'name', 'id'}, set(modelmapper.mappingfields.keys()))

    def test_no_exclude_or_include(self):
        modelmapper = ievv_elasticsearch2.Modelmapper(model_class=ModelmapperModel,
                                                      automap_fields=True)
        self.assertEqual({'char', 'text', 'smallint', 'xint', 'bigint', 'xfloat', 'xboolean', 'date', 'datetime', 'parent'},
                         set(modelmapper.mappingfields.keys()))

    def test_exclude(self):
        modelmapper = ievv_elasticsearch2.Modelmapper(model_class=ModelmapperModel,
                                                      automap_fields=True,
                                                      exclude=['char', 'text'])
        self.assertEqual({'smallint', 'xint', 'bigint', 'xfloat', 'xboolean', 'date', 'datetime', 'parent'},
                         set(modelmapper.mappingfields.keys()))

    def test_include(self):
        modelmapper = ievv_elasticsearch2.Modelmapper(model_class=ModelmapperModel,
                                                      automap_fields=True,
                                                      include=['char', 'text'])
        self.assertEqual({'char', 'text'},
                         set(modelmapper.mappingfields.keys()))

    def test_include_and_exclude_error(self):
        with self.assertRaises(ValueError):
            ievv_elasticsearch2.Modelmapper(model_class=ModelmapperModel,
                                            automap_fields=True,
                                            include=['char', 'text'],
                                            exclude=['date'])


class TestModelmapperToDict(test.TestCase):
    def test_simple_field_types(self):
        parent = mommy.make(ModelMapperForeignKeyModel)
        testdatetime = datetimeutils.default_timezone_datetime(2015, 12, 24, 18, 30)
        testobject = mommy.make(ModelmapperModel,
                                char='Char',
                                text='Text',
                                smallint=5,
                                xint=10,
                                bigint=20,
                                xfloat=0,
                                xboolean=True,
                                date=testdatetime.date(),
                                datetime=testdatetime,
                                parent=parent)
        self.assertEqual(
            {'char': 'Char',
             'text': 'Text',
             'smallint': 5,
             'xint': 10,
             'bigint': 20,
             'xfloat': 0,
             'xboolean': True,
             'date': testdatetime.date(),
             'datetime': testdatetime,
             'parent': parent.id},
            AutomappedDocType.modelmapper.to_dict(testobject, with_meta=False))

    def test_with_meta_true(self):
        testobject = mommy.make(ModelmapperModel)
        self.assertEqual(
            {'id': testobject.id},
            AutomappedDocType.modelmapper.to_dict(testobject)['meta'])

    def test_foreign_key_object_mapping(self):
        testobject = mommy.make(ModelmapperModel, parent__name='Test name')
        self.assertEqual(
            {'parent': {'name': 'Test name'}},
            WithForeignKeyObjectDocType.modelmapper.to_dict(testobject, with_meta=False))

    def test_foreign_key_prefix_mapping(self):
        testobject = mommy.make(ModelmapperModel, parent__name='Test name')
        self.assertEqual(
            {'parent__name': 'Test name'},
            WithForeignKeyPrefixDocType.modelmapper.to_dict(testobject, with_meta=False))

    def test_onetomany_nested_mapping(self):
        testobject = mommy.make(ModelmapperModel)
        mommy.make(ModelMapperChildModel, parent=testobject, size=10)
        mommy.make(ModelMapperChildModel, parent=testobject, size=20)
        self.assertEqual(
            {'children': [{'size': 10}, {'size': 20}]},
            OneToManyNestedMappingDocType.modelmapper.to_dict(testobject, with_meta=False))

    def test_onetomany_id_array_mapping(self):
        testobject = mommy.make(ModelmapperModel)
        child1 = mommy.make(ModelMapperChildModel, parent=testobject, size=10)
        child2 = mommy.make(ModelMapperChildModel, parent=testobject, size=20)
        self.assertEqual(
            {'children': [child1.id, child2.id]},
            OneToManyIdArrayMappingDocType.modelmapper.to_dict(testobject, with_meta=False))


class TestModelmapperToDoctypeObject(test.TestCase):
    def test_simple_field_types(self):
        parent = mommy.make(ModelMapperForeignKeyModel)
        testdatetime = datetimeutils.default_timezone_datetime(2015, 12, 24, 18, 30)
        testobject = mommy.make(ModelmapperModel,
                                char='Char',
                                text='Text',
                                smallint=5,
                                xint=10,
                                bigint=20,
                                xfloat=0,
                                xboolean=True,
                                date=testdatetime.date(),
                                datetime=testdatetime,
                                parent=parent)
        doctype_object = AutomappedDocType.modelmapper.to_doctype_object(testobject)
        self.assertEqual(testobject.id, doctype_object.meta.id)
        self.assertEqual('Char', doctype_object.char)
        self.assertEqual('Text', doctype_object.text)
        self.assertEqual(5, doctype_object.smallint)
        self.assertEqual(10, doctype_object.xint)
        self.assertEqual(20, doctype_object.bigint)
        self.assertEqual(0, doctype_object.xfloat)
        self.assertEqual(True, doctype_object.xboolean)
        self.assertEqual(testdatetime.date(), doctype_object.date)
        self.assertEqual(testdatetime, doctype_object.datetime)
        self.assertEqual(parent.id, doctype_object.parent)

    def test_foreign_key_object_mapping(self):
        testobject = mommy.make(ModelmapperModel, parent__name='Test name')
        doctype_object = WithForeignKeyObjectDocType.modelmapper.to_doctype_object(testobject)
        self.assertEqual(
            {'name': 'Test name'},
            doctype_object.parent)

    def test_foreign_key_prefix_mapping(self):
        testobject = mommy.make(ModelmapperModel, parent__name='Test name')
        self.assertEqual(
            {'parent__name': 'Test name'},
            WithForeignKeyPrefixDocType.modelmapper.to_dict(testobject, with_meta=False))
