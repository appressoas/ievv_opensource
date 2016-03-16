from django.db import models
from future.utils import with_metaclass


class Mapping(object):
    """
    Base class for all Django field to ElasticSearch field mappings.
    """

    #: If this is ``True``, the response from :meth:`.to_doctype_value` is expected to be
    #: a dict, and that dict is merged into the document instead of added as a single key, value pair.
    merge_into_document = False

    def __init__(self, modelfieldname=None):
        self.modelfieldname = modelfieldname
        # Automatically set to the attribute name by ModelmapperMeta and Modelmapper.automap_field()
        self.doctypefieldname = None

    def _set_doctypefieldname(self, doctypefieldname):
        self.doctypefieldname = doctypefieldname
        if not self.modelfieldname:
            self.modelfieldname = doctypefieldname

    def to_doctype_value(self, modelvalue):
        return modelvalue

    def prettyformat(self, model_class=None):
        if model_class:
            modelfield = model_class._meta.get_field(self.modelfieldname)
            modelfield_pretty = '{}({})'.format(modelfield.__class__.__name__, self.modelfieldname)
        else:
            modelfield_pretty = self.modelfieldname
        return '{}({} <-> {})'.format(self.__class__.__name__, modelfield_pretty, self.doctypefieldname)

    def get_doctype_fieldnames_list(self):
        return [self.doctypefieldname]

    def validate_mapping(self, doctype_class, doctype_fieldnames):
        for doctypefieldname in self.get_doctype_fieldnames_list():
            if doctypefieldname not in doctype_fieldnames:
                raise AttributeError(
                    '{mappingfield} is mapped to '
                    '{doctype_class_module}.{doctype_class_name}.{doctypefieldname} which does not exist.'.format(
                        mappingfield=self,
                        doctype_class_module=doctype_class.__module__,
                        doctype_class_name=doctype_class.__name__,
                        doctypefieldname=doctypefieldname
                    )
                )

    def __str__(self):
        return self.prettyformat()


class StringMapping(Mapping):
    """
    Mapping suitable to string fields (CharField, TextField).
    """


class IntegerMapping(Mapping):
    """
    Mapping suitable for integer fields.
    """


class SmallIntegerMapping(IntegerMapping):
    """
    Mapping suitable for small integer fields.
    """


class BigIntegerMapping(IntegerMapping):
    """
    Mapping suitable for big integer fields.
    """


class BooleanMapping(Mapping):
    """
    Mapping suitable for boolean fields.
    """


class FloatMapping(Mapping):
    """
    Mapping suitable for float fields.
    """


class DoubleMapping(Mapping):
    """
    Mapping suitable for double fields.
    """


class DateMapping(Mapping):
    """
    Mapping suitable for date fields.
    """


class DateTimeMapping(Mapping):
    """
    Mapping suitable for datetime fields.
    """


class ForeignKeyObjectMapping(Mapping):
    """
    Mapping suitable for ForeignKey fields that you want to
    map as a nested object in the DocType.
    """
    def __init__(self, modelmapper, modelfieldname=None):
        super(ForeignKeyObjectMapping, self).__init__(modelfieldname=modelfieldname)
        self.modelmapper = modelmapper

    def to_doctype_value(self, modelvalue):
        return self.modelmapper.to_dict(modelvalue)


class ForeignKeyPrefixMapping(Mapping):
    """
    Mapping suitable for ForeignKey fields that you want to
    map as prefixed document attributes in the DocType.
    """
    merge_into_document = True

    def __init__(self, modelmapper, prefix=None, modelfieldname=None):
        """
        Args:
            modelmapper: A :class:`.Modelmapper` object for mapping of the foreignkey fields.
            prefix: An optional prefix. Defaults to ``<doctypefieldname>__``.
            modelfieldname: The fieldname in the model.
        """
        super(ForeignKeyPrefixMapping, self).__init__(modelfieldname=modelfieldname)
        self.modelmapper = modelmapper
        self.prefix = prefix

    def get_prefix(self):
        if self.prefix is None:
            prefix = '{}__'.format(self.doctypefieldname)
        else:
            prefix = self.prefix
        return prefix

    def to_doctype_value(self, modelvalue):
        prefix = self.get_prefix()
        raw_output = self.modelmapper.to_dict(modelvalue)
        prefixed_output = {}
        for key, value in raw_output.items():
            prefixed_output['{}{}'.format(prefix, key)] = value
        return prefixed_output

    def get_doctype_fieldnames_list(self):
        prefix = self.get_prefix()
        return ['{}{}'.format(prefix, mappingfield.doctypefieldname)
                for mappingfield in self.modelmapper]


class ModelmapperMeta(type):
    """
    Metaclass for :class:`.DocType`.
    """
    def __new__(cls, name, parents, attrs):
        mappingfields = {}
        for key, value in attrs.items():
            if isinstance(value, Mapping):
                mappingfield = value
                mappingfield._set_doctypefieldname(doctypefieldname=key)
                mappingfields[mappingfield.modelfieldname] = mappingfield

        attrs['_explicit_mappingfields'] = mappingfields
        model_to_doctype_class = super(ModelmapperMeta, cls).__new__(cls, name, parents, attrs)
        return model_to_doctype_class


class Modelmapper(with_metaclass(ModelmapperMeta)):
    """
    Makes it easy to convert a Django model to a :class:`ievv_opensource.ievv_elasticsearch2.doctype.DocType`.
    """
    def __init__(self, model_class, automap_fields=False, doctype_class=None):
        self.model_class = model_class
        self.doctype_class = None
        self.mappingfields = self._explicit_mappingfields.copy()
        self._automap_fields = automap_fields
        if doctype_class:
            self.set_doctype_class(doctype_class=doctype_class)
        if self._automap_fields:
            self.automap_fields()

    def set_doctype_class(self, doctype_class):
        doctype_fieldnames = {fieldname for fieldname in doctype_class._doc_type.mapping}
        for mappingfield in self.mappingfields.values():
            mappingfield.validate_mapping(doctype_class=doctype_class,
                                          doctype_fieldnames=doctype_fieldnames)
        self.doctype_class = doctype_class

    def modelfield_to_mappingfieldclass(self, modelfield):
        """
        Gets a model field, and returns a :class:`.Mapping` subclass
        to use for that field. Used by :meth:`.automap_fields`.

        You can override this to add support for your own Django model fields,
        or to change how fields are mapped.

        Args:
            modelfield: A :class:`django.db.models.fields.Field` object.

        Returns:
            Mapping: The :class:`.Mapping` subclass to use for the provided modelfield.
        """
        if isinstance(modelfield, models.CharField):
            return StringMapping
        elif isinstance(modelfield, models.TextField):
            return StringMapping
        elif isinstance(modelfield, models.ForeignKey):
            return BigIntegerMapping
        elif isinstance(modelfield, models.BigIntegerField):
            return BigIntegerMapping
        elif isinstance(modelfield, models.SmallIntegerField):
            return SmallIntegerMapping
        elif isinstance(modelfield, models.IntegerField):
            return IntegerMapping
        elif isinstance(modelfield, models.BooleanField):
            return BooleanMapping
        elif isinstance(modelfield, models.FloatField):
            # We map FloatField to DoubleMapping because FloatField is
            # mapped to a DOUBLE in SQL.
            return DoubleMapping
        elif isinstance(modelfield, models.DateTimeField):
            return DateTimeMapping
        elif isinstance(modelfield, models.DateField):
            return DateMapping
        else:
            return None

    def automap_field(self, modelfield):
        """
        Called by :meth:`.automap_field` for each field in the model.

        You normally want to override :meth:`.modelfield_to_mappingfieldclass` instead of this
        method.

        Args:
            modelfield: The :class:`django.db.models.fields.Field` to automap.
        """
        mappingfieldclass = self.modelfield_to_mappingfieldclass(modelfield=modelfield)
        if mappingfieldclass:
            modelfieldname = modelfield.name
            if issubclass(mappingfieldclass, IntegerMapping) and isinstance(modelfield, models.ForeignKey):
                modelfieldname = '{}_id'.format(modelfield.name)
            mappingfield = mappingfieldclass()
            mappingfield._set_doctypefieldname(doctypefieldname=modelfieldname)
            self.mappingfields[modelfieldname] = mappingfield

    def automap_fields(self):
        """
        Update the mapping with automapped fields. This is called in ``__init__`` if
        ``automap_fields=True``. Ignores manually mapped fields.

        You can override this, but you will most likely rather want to override
        :meth:`.modelfield_to_mappingfieldclass` or :meth:`.automap_field`.
        """
        for modelfield in self.model_class._meta.get_fields():
            if modelfield.name not in self.mappingfields:
                self.automap_field(modelfield=modelfield)

    def to_dict(self, modelobject):
        """
        Convert the provided ``modelobject`` into dict.

        Uses :meth:`.Mapping.to_doctype_value` to convert the values.

        Args:
            modelobject: A Django data model object.

        Returns:
            dict: A dict representing data for the document.
        """
        dct = {}
        for mappingfield in self.mappingfields.values():
            modelvalue = getattr(modelobject, mappingfield.modelfieldname)
            doctype_value = mappingfield.to_doctype_value(modelvalue)
            if mappingfield.merge_into_document:
                dct.update(doctype_value)
            else:
                dct[mappingfield.doctypefieldname] = doctype_value
        return dct

    def to_doctype_object(self, modelobject):
        """
        Convert a Django data model object into a DocType object.

        Args:
            modelobject: A Django data model object.

        Returns:
            DocType: A DocType object.
        """
        return self.doctype_class(**self.to_dict(modelobject=modelobject))

    def prettyformat(self, separator='\n', prefix='- '):
        """
        Prettyformat the mapping. Useful for debugging.
        """
        output = separator.join('{}{}'.format(prefix, mappingfield.prettyformat(model_class=self.model_class))
                                for mappingfield in self.mappingfields.values())
        if output:
            return output
        else:
            return 'NO MAPPINGS'

    def __str__(self):
        return self.prettyformat(separator=', ', prefix='')

    def get_mappingfield_by_modelfieldname(self, modelfieldname, fallback=None):
        """
        Get mappingfield by model field name.

        Args:
            modelfieldname: Name of a model field.
            fallback: Fallback value if the model field does not exist. Defaults to ``None``.

        Returns:
            Mapping: A :class:`.Mapping` object.
        """
        return self.mappingfields.get(modelfieldname, fallback)

    def __iter__(self):
        """
        Iterate over mappingfields in this Modelmapper.
        """
        return iter(self.mappingfields.values())
