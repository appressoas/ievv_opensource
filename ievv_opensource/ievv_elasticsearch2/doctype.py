import inspect
import logging

import elasticsearch_dsl
from django.conf import settings
from future.utils import with_metaclass

from ievv_opensource.utils.singleton import Singleton
from .indexupdater import IndexUpdater
from .modelmapper import Modelmapper
from .search import Search

logger = logging.getLogger()


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

    Examples:

        Iterate all the :class:`.DocType` classes in the registry (does not include abstract
        doctypes)::

            from ievv_opensource import ievv_elasticsearch2
            registry = ievv_elasticsearch2.DocTypeRegistry.get_instance()
            for doctype_class in registry.get_model_doctypes_iterator():
                print(doctype_class)
    """
    def __init__(self):
        super(DocTypeRegistry, self).__init__()
        self._doctypes = []
        self._model_doctypes = []
        self._abstract_doctypes = []
        self._default_index_to_doctype_class_map = {}

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

    def __add_doctype_class_to_index_map(self, doctype_class):
        default_index = doctype_class.get_doc_type_options().index
        if default_index:
            doctypes_in_index = self._default_index_to_doctype_class_map.get(default_index, [])
            doctypes_in_index.append(doctype_class)
            self._default_index_to_doctype_class_map[default_index] = doctypes_in_index

    def add(self, doctype_class):
        """
        Add a :class:`.DocType` to the registry.

        You need to call this from the ready()-method of your AppConfig.

        Args:
            doctype_class: A :class:`.DocType` subclass.
        """
        if doctype_class.is_abstract_doctype:
            self._abstract_doctypes.append(doctype_class)
        else:
            self._doctypes.append(doctype_class)
            if issubclass(doctype_class, ModelDocType):
                self._model_doctypes.append(doctype_class)
            doctype_class.ievvinitialize()
            self.__add_doctype_class_to_index_map(doctype_class=doctype_class)


class DocTypeMeta(type):
    """
    Metaclass for :class:`.DocType`.
    """
    def __new__(mcs, name, bases, dct):
        is_abstract_doctype = dct.get('is_abstract_doctype', False)
        dct['is_abstract_doctype'] = is_abstract_doctype
        return super(DocTypeMeta, mcs).__new__(mcs, name, bases, dct)


class UnIevvInitializedDocTypeError(Exception):
    """
    Raised when trying to use a :class:`.DocType` before
    :meth:`.DocType.ievvinitialize` has been called.
    """


class DocType(with_metaclass(DocTypeMeta, object)):
    """
    Base class that you subclass to define an ElasticSearch doctype.

    Refer to :doc:`ievv_elasticsearch2` for examples.
    """
    is_abstract_doctype = True
    _has_successfully_executed_ievvinitialize = False

    #: If this is ``True``, the doctype is a base class for other doctypes, and
    #: never instantiated. An abstract DocType is not fully configured
    #: (:meth:`~.DocType.setup` returns without doing anything), and
    #: it is registered as an abstract doctype in :class:`.DocTypeRegistry`.
    #: This is ``False`` by default for subclasses, and it is not inherited, so you
    #: have to set this explicitly to ``True`` for every abstract doctype class.

    @classmethod
    def __initialize_searchobject(cls, attributename):
        searchclass = getattr(cls, attributename).__class__
        searchobject = searchclass(
            using=cls.elasticsearch_dsl_doctype_class._doc_type.using,
            index=cls.elasticsearch_dsl_doctype_class._doc_type.index,
            doc_type={cls.elasticsearch_dsl_doctype_class._doc_type.name: cls.elasticsearch_dsl_doctype_class.from_es},
        )
        setattr(cls, attributename, searchobject)

    @classmethod
    def ievvinitialize_get_elasticsearch_dsl_doctype_base_class(cls):
        return elasticsearch_dsl.DocType

    @classmethod
    def __get_manually_added_doctype_fields(cls):
        doctype_fields = {}
        for name, value in inspect.getmembers(cls):
            if isinstance(value, elasticsearch_dsl.Field):
                doctype_fields[name] = value
                delattr(cls, name)
        return doctype_fields

    @classmethod
    def ievvinitialize_create_doctype_class(cls):
        attributes = {}
        attributes.update(cls.doctype_fields)
        if hasattr(cls, 'Meta'):
            attributes['Meta'] = cls.Meta
            delattr(cls, 'Meta')

        attributes['_autocreated_by_ievv_elasticsearch'] = True
        name = '{}Dsl'.format(cls.__name__)
        cls.elasticsearch_dsl_doctype_class = type(
            name, (cls.ievvinitialize_get_elasticsearch_dsl_doctype_base_class(),), attributes)

    @classmethod
    def ievvinitialize_searchobjects(cls):
        if not hasattr(cls, 'objects'):
            cls.objects = Search()
        for name, value in inspect.getmembers(cls):
            if isinstance(value, Search):
                cls.__initialize_searchobject(attributename=name)

    @classmethod
    def ievvinitialize_indexupdater(cls):
        if hasattr(cls, 'indexupdater'):
            cls.indexupdater = cls.indexupdater.clone()
        else:
            cls.indexupdater = IndexUpdater()
        cls.indexupdater.set_doctype_class(doctype_class=cls)

    @classmethod
    def ievvinitialize_create_modelmapper(cls):
        if hasattr(cls, 'modelmapper'):
            cls.modelmapper = cls.modelmapper.clone()

    @classmethod
    def ievvinitialize_modelmapper(cls):
        if hasattr(cls, 'modelmapper'):
            cls.modelmapper.set_doctype_class(doctype_class=cls)

    @classmethod
    def ievvinitialize(cls):
        if cls._has_successfully_executed_ievvinitialize:
            return
        cls.doctype_fields = cls.__get_manually_added_doctype_fields()
        cls.ievvinitialize_create_modelmapper()
        cls.ievvinitialize_create_doctype_class()
        cls.ievvinitialize_modelmapper()
        cls.ievvinitialize_searchobjects()
        cls.ievvinitialize_indexupdater()
        cls._has_successfully_executed_ievvinitialize = True

    @classmethod
    def ievvinitialize_and_create_in_index(cls):
        if not getattr(settings, 'IEVV_ELASTICSEARCH2_TESTMODE', False):
            raise Exception('Can not use ievvinitialize_and_create_in_index() unless '
                            'the IEVV_ELASTICSEARCH2_TESTMODE-setting is set to True.')
        cls.ievvinitialize()
        cls.init()

    #
    #
    # Mirror classmethods on elasticsearch_dsl.DocType
    #
    #

    @classmethod
    def __classmethod_use_before_ievvinitialize_check(cls, methodname):
        if not cls._has_successfully_executed_ievvinitialize:
            raise UnIevvInitializedDocTypeError(
                'Can not use {}.{}.{} before the DocType has been initialized with ievvinitialize().'.format(
                    cls.__module__, cls.__name__, methodname
                ))

    @classmethod
    def init(cls, index=None, using=None):
        cls.__classmethod_use_before_ievvinitialize_check('init')
        cls.elasticsearch_dsl_doctype_class.init(index=index, using=using)

    @classmethod
    def get(cls, id, using=None, index=None, **kwargs):
        cls.__classmethod_use_before_ievvinitialize_check('get')
        return cls.elasticsearch_dsl_doctype_class.get(
            id=id, using=using, index=index, **kwargs)

    #
    #
    # Convenience class methods
    #
    #

    @classmethod
    def get_doc_type_options(cls):
        return cls.elasticsearch_dsl_doctype_class._doc_type

    # @classmethod
    # def get_all_fieldnames_set(cls):
    #     all_fieldnames = set()
    #     for fieldname in cls.get_doc_type_options().mapping:
    #         all_fieldnames.add(fieldname)
    #     return all_fieldnames

    def __init__(self, **kwargs):
        if not self.__class__._has_successfully_executed_ievvinitialize:
            raise UnIevvInitializedDocTypeError(
                'Can not initialize {}.{} it has been been initialized with ievvinitialize().'.format(
                    self.__class__.__module__, self.__class__.__name__))
        self.kwargs = kwargs
        self.elasticsearch_dsl_doctype = self.elasticsearch_dsl_doctype_class(**kwargs)

    #
    #
    # Make attribute access work as close to working with
    # elasticsearch_dsl.DocType as possible.
    #
    #

    def __getattr__(self, name):
        if name in self.__class__.doctype_fields:
            return getattr(self.elasticsearch_dsl_doctype, name)
        else:
            raise AttributeError('No attribute named {}'.format(name))

    def __setattr__(self, name, value):
        if name in self.__class__.doctype_fields:
            return setattr(self.elasticsearch_dsl_doctype, name, value)
        else:
            return super(DocType, self).__setattr__(name, value)

    @property
    def meta(self):
        return self.elasticsearch_dsl_doctype.meta

    @property
    def _id(self):
        return self.elasticsearch_dsl_doctype.meta.id

    @_id.setter
    def _id(self, value):
        self.elasticsearch_dsl_doctype.meta.id = value

    #
    #
    # Mirror instance methods from elasticsearch_dsl.DocType
    #
    #

    def delete(self, **kwargs):
        return self.elasticsearch_dsl_doctype.delete(**kwargs)

    def to_dict(self, **kwargs):
        return self.elasticsearch_dsl_doctype.to_dict(**kwargs)

    def update(self, **kwargs):
        return self.elasticsearch_dsl_doctype.update(**kwargs)

    def save(self, **kwargs):
        self.elasticsearch_dsl_doctype.save(**kwargs)


    #
    #
    # Convenience instance methods
    #
    #

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
        self.elasticsearch_dsl_doctype._get_connection(using=using).flush()


class ModelDocType(DocType):
    is_abstract_doctype = True

    @classmethod
    def ievvinitialize_create_modelmapper(cls):
        super(ModelDocType, cls).ievvinitialize_create_modelmapper()

        model_class = getattr(cls, 'model_class', None)
        if model_class is not None:
            if not hasattr(cls, 'modelmapper'):
                cls.modelmapper = Modelmapper(model_class=model_class, automap_fields=True)
            for doctypefieldname, doctypefield in cls.modelmapper.automake_doctype_fields().items():
                if doctypefieldname not in cls.doctype_fields:
                    cls.doctype_fields[doctypefieldname] = doctypefield
