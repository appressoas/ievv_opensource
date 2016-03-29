import logging

import elasticsearch_dsl
from elasticsearch_dsl.document import DocTypeMeta as ElasticSearchDocTypeMeta
from future.utils import with_metaclass

from ievv_opensource.utils.singleton import Singleton
from .indexupdater import IndexUpdater
from .modelmapper import Modelmapper
from .search import Search

logger = logging.getLogger()


class DocTypeConfigurationError(Exception):
    """
    Raised when a :class:`.DocType` is configured incorrectly.
    """


def _update_searchobject_for_doctype(doctype_class, attributename):
    searchclass = getattr(doctype_class, attributename).__class__
    searchobject = searchclass(
        using=doctype_class._doc_type.using,
        index=doctype_class._doc_type.index,
        doc_type={doctype_class._doc_type.name: doctype_class.from_es},
    )
    setattr(doctype_class, attributename, searchobject)


class DocTypeRegistry(Singleton):
    """
    Registry of all :class:`.DocType` classes.

    The reason for a registry of all DocType classes is to make it possible
    to perform automatic configuration/mapping/setup after initialization
    of other resources, such as model initialization. The framework uses
    this internally for the :class:`.ModelDocType` when the modelmapper uses
    automatic mapping of fields, but the API is public so you can use the
    registry in your own ``AppConfig.ready(...)`` methods.

    The registry divides doctypes into 3 groups:

    - Subclasses of :class:`.DocType` (including subclasses of :class:`.ModelDocType`).
      This group of doctypes can be accessed using :meth:`.get_doctypes_iterator`.
    - Subclasses of :class:`.ModelDocType`.
      This group of doctypes can be accessed using :meth:`.get_model_doctypes_iterator`.
    - Subclasses of :class:`.DocType` (including subclasses of :class:`.ModelDocType`,
      and the base classes (DocType and ModelDocType)) with :obj:`~.DocType.abstract`
      set to ``True``.
      This group of doctypes can be accessed using :meth:`.get_abstract_doctypes_iterator`.
    """
    def __init__(self):
        super(DocTypeRegistry, self).__init__()
        self._doctypes = []
        self._model_doctypes = []
        self._abstract_doctypes = []

    def get_doctypes_iterator(self):
        """
        Get an iterable of all registered :class:`.DocType` subclasses,
        including :class:`.ModelDocType` subclasses.
        Does not include :obj:`~.DocType.abstract` doctypes.
        """
        return iter(self._doctypes)

    def get_model_doctypes_iterator(self):
        """
        Get an iterable of all registered :class:`.ModelDocType` subclasses.
        """
        return iter(self._doctypes)

    def get_abstract_doctypes_iterator(self):
        """
        Get an iterable of all registered :obj:`~.DocType.abstract`
        :class:`.DocType` subclasses.
        """
        return iter(self._abstract_doctypes)

    def _add_doctype(self, doctype_class):
        """
        Add a :class:`.DocType` to the registry.

        Called automatically by :class:`.DocTypeMeta`, so you never have
        to call this yourself.

        Args:
            doctype_class: A :class:`.DocType` subclass.
        """
        if doctype_class.abstract:
            self._abstract_doctypes.append(doctype_class)
        else:
            self._doctypes.append(doctype_class)

    def _add_model_doctype(self, doctype_class):
        """
        Add a :class:`.ModelDocType` to the registry.

        Called automatically by :class:`.ModelDocTypeMeta`, so you never have
        to call this yourself.

        Args:
            doctype_class: A :class:`.ModelDocType` subclass.
        """
        if not doctype_class.abstract:
            self._model_doctypes.append(doctype_class)


class DocTypeMeta(ElasticSearchDocTypeMeta):
    """
    Metaclass for :class:`.DocType`.
    """
    def __new__(cls, name, parents, dct):
        abstract = dct.get('abstract', False)
        dct['abstract'] = abstract
        doctype_class = super(DocTypeMeta, cls).__new__(cls, name, parents, dct)

        if 'objects' not in dct:
            doctype_class.objects = Search()
            _update_searchobject_for_doctype(doctype_class=doctype_class,
                                             attributename='objects')
        for key, value in dct.items():
            if isinstance(value, Search):
                _update_searchobject_for_doctype(doctype_class=doctype_class,
                                                 attributename=key)
        if hasattr(doctype_class, 'indexupdater'):
            doctype_class.indexupdater = doctype_class.indexupdater.clone()
        else:
            doctype_class.indexupdater = IndexUpdater()
        doctype_class.indexupdater.set_doctype_class(doctype_class=doctype_class)

        if hasattr(doctype_class, 'modelmapper'):
            doctype_class.modelmapper = doctype_class.modelmapper.copy()
            doctype_class.modelmapper.set_doctype_class(doctype_class=doctype_class)

        DocTypeRegistry.get_instance()._add_doctype(doctype_class=doctype_class)
        return doctype_class


class DocType(with_metaclass(DocTypeMeta, elasticsearch_dsl.DocType)):
    #: If this is ``True``, the doctype is a base class for other doctypes, and
    #: never instantiated. An abstract DocType is not fully configured, and
    #: it is registered as an abstract doctype in :class:`.DocTypeRegistry`.
    #: This is ``False`` by default for subclasses, and it is not inherited, so you
    #: have to set this explicitly to ``True`` for every abstract doctype class.
    abstract = True

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


class ModelDocTypeMeta(DocTypeMeta):
    def __new__(cls, name, parents, dct):
        modelmapper = None
        model_class = dct.get('model_class', None)
        if model_class is not None:
            if 'modelmapper' in dct:
                modelmapper = dct['modelmapper'].copy()
            else:
                modelmapper = Modelmapper(model_class=model_class, automap_fields=True)
                dct['modelmapper'] = modelmapper
            for doctypefieldname, doctypefield in modelmapper.automake_doctype_fields().items():
                if doctypefieldname not in dct:
                    dct[doctypefieldname] = doctypefield
        doctype_class = super(ModelDocTypeMeta, cls).__new__(cls, name, parents, dct)
        if modelmapper:
            modelmapper.set_doctype_class(doctype_class=doctype_class)

        DocTypeRegistry.get_instance()._add_model_doctype(doctype_class=doctype_class)
        return doctype_class


class ModelDocType(with_metaclass(ModelDocTypeMeta, DocType)):
    model_class = None
    abstract = True
