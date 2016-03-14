import elasticsearch_dsl
from django import test
from elasticsearch_dsl.connections import connections

from ievv_opensource import ievv_elasticsearch2


class PersonDocType(ievv_elasticsearch2.DocType):
    indexupdater = ievv_elasticsearch2.IndexUpdater()
    name = elasticsearch_dsl.String()

    class Meta:
        index = 'main'


class TestIndexUpdater(test.TestCase):
    def setUp(self):
        self.es = connections.get_connection()
        self.es.indices.delete(index='_all')
        self.es.indices.flush(index='_all')

    def test_bulk_index_single(self):
        PersonDocType.init()
        person = PersonDocType(name='Test')
        person.meta.id = 1
        PersonDocType.indexupdater.bulk_index([person])
        person = person.get_from_index()
        self.assertEqual('Test', person.name)

    def test_bulk_index_multiple(self):
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
