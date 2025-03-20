
from django import template

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