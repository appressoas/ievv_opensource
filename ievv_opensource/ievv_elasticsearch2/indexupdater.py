import elasticsearch.helpers
from elasticsearch_dsl.connections import connections


class IndexUpdater(object):
    """
    Makes it easier to (bulk)index and re-index documents for a DocType.

    .. attribute:: doctype_class

        The :class:`ievv_opensource.ievv_elasticsearch2.doctype.DocType` subclass
        this IndexUpdater is for. See :meth:`.set_doctype_class`.
    """
    PRIORITY_LOW = 'low'
    PRIORITY_MEDIUM = 'medium'
    PRIORITY_HIGH = 'high'

    def __init__(self, doctype_class=None):
        """
        Args:
            doctype_class: If this is not ``None``, __init__ will call :meth:`.set_doctype_class`
                with this as input.
        """
        self.doctype_class = None
        if doctype_class:
            self.set_doctype_class(doctype_class=doctype_class)

    def set_doctype_class(self, doctype_class):
        """
        Set :attr:`~.IndexUpdater.doctype_class`.

        You normally do not call this directly - this is called during class creation
        of :class:`ievv_opensource.ievv_elasticsearch2.doctype.DocType` if the
        DocType subclass has an ``indexupdater`` attribute. Read more about this
        in the docs for :class:`ievv_opensource.ievv_elasticsearch2.doctype.DocTypeMeta`.

        Args:
            doctype_class: The :class:`ievv_opensource.ievv_elasticsearch2.doctype.DocType` subclass
                to set as the ``doctype_class``.
        """
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

    def __iterate_bulk_index_actions(self, doctype_object_iterable):
        for doctype_object in doctype_object_iterable:
            yield doctype_object.to_dict(include_meta=True)

    def bulk_index(self, doctype_object_iterable, using=None):
        """
        Bulk index the provided doctype objects using :func:`elasticsearch.helpers.bulk`.

        Args:
            doctype_object_iterable: An iteratable of DocType objects.
            using: See :meth:`.get_connection`.
        """
        elasticsearch.helpers.bulk(
            client=self.get_connection(using=using),
            actions=self.__iterate_bulk_index_actions(doctype_object_iterable=doctype_object_iterable))

    def __doctype_object_iterable_from_queryset(self, queryset):
        for modelobject in queryset.all():  # TODO: iterator() instead?
            yield self.doctype_class.modelmapper.to_doctype_object(modelobject=modelobject)

    def bulk_index_model_ids(self, id_iterable, using=None):
        """
        Bulk index the provided IDs using :func:`elasticsearch.helpers.bulk`.

        This only works if the :attr:`.IndexUpdater.doctype_class` has a ``model_class``
        attribute, so this is intended for doctypes that subclass
        :class:`ievv_opensource.ievv_elasticsearch2.doctype.ModelDocType`.

        Args:
            id_iterable: An iteratable of Django model object IDs.
            using: See :meth:`.get_connection`.
        """
        if not hasattr(self.doctype_class, 'model_class'):
            raise AttributeError(
                'The doctype_class ({}.{}) for {}.{} does not have a model_class attribute.'.format(
                    self.doctype_class.__module__, self.doctype_class.__name__,
                    self.__class__.__module__, self.__class__.__name__))
        queryset = self.doctype_class.model_class.objects.filter(id__in=id_iterable)
        doctype_object_iterable = self.__doctype_object_iterable_from_queryset(queryset=queryset)
        return self.bulk_index(doctype_object_iterable=doctype_object_iterable, using=using)

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
                means reindex ALL documents. The intention of this argument is to enable you
                to segment you data into different priorities
                by overriding :meth:`.iterate_doctype_objects_for_reindexing`. Unless your app
                has very special needs, we recommend that you use :obj:`.IndexUpdater.PRIORITY_LOW`,
                :obj:`.IndexUpdater.PRIORITY_MEDIUM` and :obj:`.IndexUpdater.PRIORITY_HIGH` as constants
                for priorities. This is enough for most needs, and using a common set of priorities
                makes for more reusable code.
            using: See :meth:`.get_connection`.
        """
        self.bulk_index(
            doctype_object_iterable=self.iterate_doctype_objects_for_reindexing(priority=priority),
            using=using)
