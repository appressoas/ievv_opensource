import elasticsearch_dsl
from django import test
from elasticsearch_dsl.connections import connections
from model_mommy import mommy

from ievv_opensource import ievv_elasticsearch2
from ievv_opensource.ievv_elasticsearch2.tests.ievv_elasticsearch2_testapp.models import ModelmapperModel


class PersonDocType(ievv_elasticsearch2.DocType):
    indexupdater = ievv_elasticsearch2.IndexUpdater()
    name = elasticsearch_dsl.String()

    class Meta:
        index = 'main'


class TestIndexUpdaterBulkIndex(test.TestCase):
    def setUp(self):
        self.es = connections.get_connection()
        self.es.indices.delete(index='_all')
        self.es.indices.flush(index='_all')

    def test_single(self):
        PersonDocType.init()
        person = PersonDocType(name='Test')
        person.meta.id = 1
        PersonDocType.indexupdater.bulk_index([person])
        person = person.get_from_index()
        self.assertEqual('Test', person.name)

    def test_multiple(self):
        PersonDocType.init()
        person1 = PersonDocType(name='Test1')
        person1.meta.id = 10
        person2 = PersonDocType(name='Test2')
        person2.meta.id = 20
        person3 = PersonDocType(name='Test3')
        person3.meta.id = 30
        PersonDocType.indexupdater.bulk_index([person1, person2, person3])

        person1 = person1.get_from_index()
        person2 = person2.get_from_index()
        person3 = person3.get_from_index()
        self.assertEqual('Test1', person1.name)
        self.assertEqual('Test2', person2.name)
        self.assertEqual('Test3', person3.name)


class AutomappedDocType(ievv_elasticsearch2.ModelDocType):
    model_class = ModelmapperModel

    class Meta:
        index = 'main'


class TestIndexUpdatedBulkIndexModelIds(test.TestCase):
    def setUp(self):
        self.es = connections.get_connection()
        self.es.indices.delete(index='_all')
        self.es.indices.flush(index='_all')

    def test_single(self):
        item = mommy.make(ModelmapperModel, char='a')
        AutomappedDocType.indexupdater.bulk_index_model_ids(id_iterable=[item.id])
        self.assertEqual('a', AutomappedDocType.get(id=item.id).char)

    def test_multiple(self):
        item1 = mommy.make(ModelmapperModel, char='a')
        item2 = mommy.make(ModelmapperModel, char='b')
        item3 = mommy.make(ModelmapperModel, char='c')
        AutomappedDocType.indexupdater.bulk_index_model_ids(id_iterable=[item1.id, item2.id, item3.id])
        self.assertEqual('a', AutomappedDocType.get(id=item1.id).char)
        self.assertEqual('b', AutomappedDocType.get(id=item2.id).char)
        self.assertEqual('c', AutomappedDocType.get(id=item3.id).char)
