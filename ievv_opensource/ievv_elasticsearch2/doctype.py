import logging

import elasticsearch_dsl
from elasticsearch_dsl.document import DocTypeMeta as ElasticSearchDocTypeMeta
from future.utils import with_metaclass

from .search import Search

logger = logging.getLogger()


def _update_searchobject_for_doctype(doctype_class, attributename):
    searchclass = getattr(doctype_class, attributename).__class__
    searchobject = searchclass(
        using=doctype_class._doc_type.using,
        index=doctype_class._doc_type.index,
        doc_type={doctype_class._doc_type.name: doctype_class.from_es},
    )
    setattr(doctype_class, attributename, searchobject)


class DocTypeMeta(ElasticSearchDocTypeMeta):
    """
    Metaclass for :class:`.DocType`.
    """

    def __new__(cls, name, parents, dct):
        doctype_class = super(DocTypeMeta, cls).__new__(cls, name, parents, dct)

        if 'objects' not in dct:
            doctype_class.objects = Search()
            _update_searchobject_for_doctype(doctype_class=doctype_class,
                                             attributename='objects')
        for key, value in dct.items():
            if isinstance(value, Search):
                # value.params()
                _update_searchobject_for_doctype(doctype_class=doctype_class,
                                                 attributename=key)
        if hasattr(doctype_class, 'indexupdater'):
            indexupdater_class = doctype_class.indexupdater.__class__
            doctype_class.indexupdater = indexupdater_class(
                doctype_class=doctype_class
            )

        return doctype_class


class DocType(with_metaclass(DocTypeMeta, elasticsearch_dsl.DocType)):
    @classmethod
    def search(cls, *args, **kwargs):
        logger.warning('You should use {classname}.objects instead of {classname}.search().'.format(
            classname=cls.__name__))
        return super(DocType, cls).search(*args, **kwargs)

    def get_from_index(self):
        """
        Get this document from the search index. Simply performs a GET on the
        ID of this document and returns the result.
        """
        return self.__class__.get(id=self.meta.id)

    def flush_index(self, using=None):
        """
        Flush the index this document belongs to.

        Useful if you need to retrieve data that was updated in the index, but
        may not be avaiable right away.

        .. warning:: You should be very careful when using
            this since it can impact performance. It is mostly useful
            for debugging and in tests.
        """
        self._get_connection(using=using).flush()
