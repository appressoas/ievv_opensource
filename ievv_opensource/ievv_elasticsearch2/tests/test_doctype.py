import elasticsearch_dsl
from django import test
from elasticsearch_dsl.connections import connections

from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.ievv_elasticsearch2.tests.ievv_elasticsearch2_testapp.models import SimpleModel


class TestDocType(test.TestCase):
    def setUp(self):
        self.es = connections.get_connection()
        self.es.indices.delete(index='_all')
        self.es.indices.flush(index='_all')

    def test_get_from_index(self):
        class MyDocType(ievv_elasticsearch2.DocType):
            name = elasticsearch_dsl.String()

            class Meta:
                index = 'main'

        MyDocType.init()
        document = MyDocType(name='Peter')
        document.meta.id = 1
        document.save()
        self.es.update(index='main', doc_type=MyDocType._doc_type.name,
                       id=1, body={'doc': {'name': 'Updated name'}})
        updated_document = document.get_from_index()
        self.assertEqual('Updated name', updated_document.name)


class TestModelDocTypeMeta(test.TestCase):
    def test_simple(self):
        class MyModelDocType(ievv_elasticsearch2.ModelDocType):
            model_class = SimpleModel
        self.assertIn('name', MyModelDocType._doc_type.mapping)
        doctype_field = MyModelDocType._doc_type.mapping['name']
        self.assertTrue(isinstance(doctype_field, elasticsearch_dsl.String))
