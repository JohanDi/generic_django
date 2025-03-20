from rest_framework import metadata
from rest_framework import serializers
from rest_framework.utils.field_mapping import ClassLookupDict


class CustomMetadata(metadata.SimpleMetadata):
    """
    Custom metadata class which provides field metadata for the resource.
    See also https://www.django-rest-framework.org/api-guide/metadata/

    This implementation does the following:
    - looks for an attribute extra_field_metadata in the serializer Meta class. This attribute should be a dictionary
    with field names as keys and dictionaries as values. A check is made to see if the field is in the dictionary
    and if so, the dictionary is merged with the default metadata.
    - adds a new field type 'fk_field' for ForeignKey fields to the metadata field definitions.
    - adds a new field type 'm2m_field' for ManyToMany fields to the metadata field definitions.
    """

    label_lookup = ClassLookupDict({
        # Newly added fields
        serializers.PrimaryKeyRelatedField: 'fk_field',
        serializers.ManyRelatedField: 'm2m_field',
        # Copied from SimpleMetadata
        serializers.Field: 'field',
        serializers.BooleanField: 'boolean',
        serializers.CharField: 'string',
        serializers.UUIDField: 'string',
        serializers.URLField: 'url',
        serializers.EmailField: 'email',
        serializers.RegexField: 'regex',
        serializers.SlugField: 'slug',
        serializers.IntegerField: 'integer',
        serializers.FloatField: 'float',
        serializers.DecimalField: 'decimal',
        serializers.DateField: 'date',
        serializers.DateTimeField: 'datetime',
        serializers.TimeField: 'time',
        serializers.DurationField: 'duration',
        serializers.ChoiceField: 'choice',
        serializers.MultipleChoiceField: 'multiple choice',
        serializers.FileField: 'file upload',
        serializers.ImageField: 'image upload',
        serializers.ListField: 'list',
        serializers.DictField: 'nested object',
        serializers.Serializer: 'nested object',
    })


    def get_field_info(self, field):
        field_info = super().get_field_info(field)
        if hasattr(field.parent.Meta, 'extra_field_metadata'):
            if field.field_name in field.parent.Meta.extra_field_metadata:
                field_info.update(field.parent.Meta.extra_field_metadata[field.field_name])
        return field_info