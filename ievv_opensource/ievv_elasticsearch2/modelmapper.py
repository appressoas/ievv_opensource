import elasticsearch_dsl
from django.core.exceptions import FieldDoesNotExist
from django.db import models
from future.utils import with_metaclass


class FieldMappingValidationError(Exception):
    """
    Superclass for exceptions raised when :meth:`.FieldMapping.validate_mapping` fails.
    """


class DoctypeFieldDoesNotExist(FieldMappingValidationError):
    """
    Raised when :meth:`.FieldMapping.validate_mapping` fails because
    the referenced doctype field does not exist on the DocType.
    """


class ModelFieldDoesNotExist(FieldMappingValidationError):
    """
    Raised when :meth:`.FieldMapping.validate_mapping` fails because
    the referenced Django model field does not exist.
    """


class FieldMapping(object):
    """
    Base class for all Django field to ElasticSearch field mappings.

    .. attribute:: doctypefieldname

        The name of the doctype field.

    .. attribute:: modelfieldname

        The name of the model field.
    """

    #: If this is ``True``, the response from :meth:`.to_doctype_value` is expected to be
    #: a dict, and that dict is merged into the document instead of added as a single key, value pair.
    merge_into_document = False

    #: The appropriate elasticearch-dsl field class to use when
    #: autocreating DocType fields from this FieldMapping.
    #: Used by :meth:`.automake_doctype_fields`.
    elasticsearchdsl_fieldclass = None

    def __init__(self, modelfieldname=None):
        self.modelfieldname = modelfieldname
        # Automatically set to the attribute name by ModelmapperMeta and Modelmapper.automap_field()
        self.doctypefieldname = None

    def _set_doctypefieldname(self, doctypefieldname):
        self.doctypefieldname = doctypefieldname
        if not self.modelfieldname:
            self.modelfieldname = doctypefieldname

    def automake_doctype_fields(self, model_class):
        """
        Create elasticsearch-dsl :class:`elasticsearch_dsl.field.Field` objects from
        this FieldMapping.

        For simple cases you do not have to override this, but instead you
        can just set :obj:`~.FieldMapping.elasticsearchdsl_fieldclass`.

        Used by :class:`ievv_opensource.ievv_elasticsearch2.doctype.ModelDocType`.

        Args:
            model_class: The Django model class.

        Returns:
            dict: A dict where the keys is the doctype field name and the values is
                :class:`elasticsearch_dsl.field.Field` objects.
        """
        return {
            self.doctypefieldname: self.elasticsearchdsl_fieldclass()
        }

    def to_doctype_value(self, modelvalue):
        """
        Convert the value stored in the model to a value compatible with
        ElasticSearch.

        Args:
            modelvalue: The value stored in the Django model.

        Returns:
            object: The converted value.
        """
        return modelvalue

    def prettyformat(self, model_class=None):
        """
        Prettyformat this FieldMapping instance.

        Args:
            model_class: If provided, more information is included in the prettyformatted output.

        Returns:
            str: Prettyformatted information about this FieldMapping.
        """
        if model_class:
            modelfield = model_class._meta.get_field(self.modelfieldname)
            modelfield_pretty = '{}({})'.format(modelfield.__class__.__name__, self.modelfieldname)
        else:
            modelfield_pretty = self.modelfieldname
        return '{}({} <-> {})'.format(self.__class__.__name__, modelfield_pretty, self.doctypefieldname)

    def get_required_doctype_fieldnames_list(self):
        """
        Get a list of doctype fieldnames this mapping maps to.

        For simple fields, this returns a list only containing :attr:`~.FieldMapping.doctypefieldname`,
        but for more complex cases where a single Django model field is mapped to multiple
        fields in the doctype, this is overridden to return multiple doctype fieldnames.
        One example of such a more complex case is the :class:`.ForeignKeyPrefixMapping`
        which maps foreignkey fields as multiple prefixed attributes on the doctype.

        Used by :meth:`.validate_mapping`. This means that you usually do not have to
        override :meth:`.validate_mapping`, but instead just have to override this method
        if your custom FieldMapping maps to multiple doctype fields.
        """
        return [self.doctypefieldname]

    def validate_mapping(self, model_class, doctype_class, doctype_fieldnames_set):
        """
        Validate the mapping, to ensure that the mapped doctype fields actually exists.

        Args:
            doctype_class: The :class:`ievv_opensource.ievv_elasticsearch2.doctype.DocType` class.
            doctype_fieldnames_set: Set of doctype fieldnames.

        Raises:
            DoctypeFieldDoesNotExist: If any of the fieldnames returned by
                :meth:`.get_required_doctype_fieldnames_list` is not in ``doctype_fieldnames_set``.
        """
        try:
            model_class._meta.get_field(self.modelfieldname)
        except FieldDoesNotExist:
            raise ModelFieldDoesNotExist(
                '{mappingfield} is mapped from '
                '{model_class_module}.{model_class_name}.{modelfieldname} which does not exist.'.format(
                    mappingfield=self,
                    model_class_module=model_class.__module__,
                    model_class_name=model_class.__name__,
                    modelfieldname=self.modelfieldname
                )
            )
        for doctypefieldname in self.get_required_doctype_fieldnames_list():
            if doctypefieldname not in doctype_fieldnames_set:
                raise DoctypeFieldDoesNotExist(
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


class StringMapping(FieldMapping):
    """
    FieldMapping suitable to string fields (CharField, TextField).
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.String


class IntegerMapping(FieldMapping):
    """
    FieldMapping suitable for integer fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Integer


class SmallIntegerMapping(IntegerMapping):
    """
    FieldMapping suitable for small integer fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Short


class BigIntegerMapping(IntegerMapping):
    """
    FieldMapping suitable for big integer fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Long


class BooleanMapping(FieldMapping):
    """
    FieldMapping suitable for boolean fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Boolean


class FloatMapping(FieldMapping):
    """
    FieldMapping suitable for float fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Float


class DoubleMapping(FieldMapping):
    """
    FieldMapping suitable for double fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Double


class DateMapping(FieldMapping):
    """
    FieldMapping suitable for date fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Date


class DateTimeMapping(FieldMapping):
    """
    FieldMapping suitable for datetime fields.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Date


class ForeignKeyObjectMapping(FieldMapping):
    """
    FieldMapping suitable for ForeignKey fields that you want to
    map as a nested object in the DocType.
    """
    elasticsearchdsl_fieldclass = elasticsearch_dsl.Object

    def __init__(self, modelmapper, modelfieldname=None):
        super(ForeignKeyObjectMapping, self).__init__(modelfieldname=modelfieldname)
        self.modelmapper = modelmapper

    def to_doctype_value(self, modelvalue):
        return self.modelmapper.to_dict(modelvalue)


class ForeignKeyPrefixMapping(FieldMapping):
    """
    FieldMapping suitable for ForeignKey fields that you want to
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

    def __prefix_dict_keys(self, dct):
        output_dict = {}
        prefix = self.get_prefix()
        for key, value in dct.items():
            output_dict['{}{}'.format(prefix, key)] = value
        return output_dict

    def automake_doctype_fields(self, model_class):
        foreignkey_doctype_fields = self.modelmapper.automake_doctype_fields()
        return self.__prefix_dict_keys(foreignkey_doctype_fields)

    def get_prefix(self):
        if self.prefix is None:
            prefix = '{}__'.format(self.doctypefieldname)
        else:
            prefix = self.prefix
        return prefix

    def to_doctype_value(self, modelvalue):
        raw_output = self.modelmapper.to_dict(modelvalue)
        return self.__prefix_dict_keys(raw_output)

    def get_required_doctype_fieldnames_list(self):
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
            if isinstance(value, FieldMapping):
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

    def automake_doctype_fields(self):
        """
        Create elasticsearch-dsl :class:`elasticsearch_dsl.field.Field` objects from
        this Modelmapper.

        Used by :class:`ievv_opensource.ievv_elasticsearch2.doctype.ModelDocType`.

        Returns:
            dict: A dict where the keys is the doctype field name and the values is
                :class:`elasticsearch_dsl.field.Field` objects.
        """
        doctype_fields = {}
        for mappingfield in self.mappingfields.values():
            doctype_fields.update(mappingfield.automake_doctype_fields(model_class=self.model_class))
        return doctype_fields

    def set_doctype_class(self, doctype_class):
        doctype_fieldnames_set = {fieldname for fieldname in doctype_class._doc_type.mapping}
        for mappingfield in self.mappingfields.values():
            mappingfield.validate_mapping(model_class=self.model_class,
                                          doctype_class=doctype_class,
                                          doctype_fieldnames_set=doctype_fieldnames_set)
        self.doctype_class = doctype_class

    def modelfield_to_mappingfieldclass(self, modelfield):
        """
        Gets a model field, and returns a :class:`.FieldMapping` subclass
        to use for that field. Used by :meth:`.automap_fields`.

        You can override this to add support for your own Django model fields,
        or to change how fields are mapped.

        Args:
            modelfield: A :class:`django.db.models.fields.Field` object.

        Returns:
            FieldMapping: The :class:`.FieldMapping` subclass to use for the provided modelfield.
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

        Uses :meth:`.FieldMapping.to_doctype_value` to convert the values.

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
            FieldMapping: A :class:`.FieldMapping` object.
        """
        return self.mappingfields.get(modelfieldname, fallback)

    def __iter__(self):
        """
        Iterate over mappingfields in this Modelmapper.
        """
        return iter(self.mappingfields.values())
