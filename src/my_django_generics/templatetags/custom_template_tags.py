
from django import template
from django.template import defaultfilters
from django.templatetags.tz import localtime

register = template.Library()

@register.filter
def get_item(obj, key):
    keys = key.split('.')
    for k in keys:
        try:
            obj = obj[k]
        except (TypeError, KeyError, IndexError):
            try:
                obj = getattr(obj, k)
            except AttributeError:
                return None
    return obj

@register.filter
def apply_format(value, format_string):
    """
    Applies a format string to a value.
    Usage: {{ value|apply_format:"format_string" }}
    """
    match format_string:
        case 'capfirst':
            return defaultfilters.capfirst(value)
        case 'title':
            return defaultfilters.title(value)
        case 'upper':
            return defaultfilters.upper(value)
        case 'lower':
            return defaultfilters.lower(value)
        case 'localtime':
            return localtime(value)
        case _:
            raise ValueError(f"Unknown format string: {format_string}")