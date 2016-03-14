import elasticsearch.helpers
from elasticsearch_dsl.connections import connections


class IndexUpdater(object):
    """
    Makes it easier to (bulk)index and re-index documents for a DocType.
    """
    def __init__(self, doctype_class=None):
        self.doctype_class = doctype_class

    def get_connection(self, using=None):
        """
        Get ElasticSearch client connection.

        Should not need to use this unless you are making a subclass and adding new features.

        Args:
            using: See :meth:`elasticsearch_dsl.connections.Connections.get_connection`.
                Defaults to the default connection for the DocType class.

        Returns:
            elasticsearch.client.Elasticsearch: An Elasticsearch object for the connection.
        """
        return connections.get_connection(using or self.doctype_class._doc_type.using)

    def __iterate_bulk_index_actions(self, doctype_object_iterator):
        for doctype_object in doctype_object_iterator:
            yield doctype_object.to_dict(include_meta=True)

    def bulk_index(self, doctype_object_iterator, using=None):
        """
        Bulk index the provided doctype objects using :func:`elasticsearch.helpers.bulk`.

        Args:
            doctype_object_iterator: An iteratable of DocType objects.
            using: See :meth:`.get_connection`.
        """
        elasticsearch.helpers.bulk(
            client=self.get_connection(using=using),
            actions=self.__iterate_bulk_index_actions(doctype_object_iterator=doctype_object_iterator))

    def iterate_doctype_objects_for_reindexing(self, priority=None):
        """
        Iterate doctype objects for :meth:`.bulk_reindex_by_priority`.

        Must be overridden in subclasses if you want to be able to reindex your documents.

        Args:
            priority: See :meth:`.bulk_reindex_by_priority`.

        Returns:
            iterator: Iterator of DocType objects.
        """
        raise NotImplementedError()

    def bulk_reindex_by_priority(self, priority=None, using=None):
        """
        Re-index documents of this DocType.

        The documents to reindex is retrieved using :meth:`.iterate_doctype_objects_for_reindexing`,
        which you must override.

        Args:
            priority: Only index items with the provided priority. Defaults to ``None`` which
                means reindex ALL documents. This library does not provide any other priority than
                ``None``, but it is designed so that you can segment you data into different priorities
                by overriding :meth:`.iterate_doctype_objects_for_reindexing`.
            using: See :meth:`.get_connection`.
        """
        self.bulk_index(
            doctype_object_iterator=self.iterate_doctype_objects_for_reindexing(priority=priority),
            using=using)
