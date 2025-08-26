from django import template, forms
from datetime import datetime, timezone

register = template.Library()

@register.filter
def is_recent(value, days=7):
    """Returns True if the datetime value is within the last X days"""
    if not value:
        return False
    now = datetime.now(timezone.utc)
    delta = now - value
    return delta.days < days

@register.filter(name='getattr')
def getattr_filter(obj, attr_name):
    """Get attribute from an object by string name"""
    return getattr(obj, attr_name, '')

@register.filter(name='attr')
def set_attr(field, attr_string):
    """Set an attribute on a form field"""
    attr_name, attr_value = attr_string.split(':')
    attrs = field.field.widget.attrs
    attrs[attr_name] = attr_value
    return field

@register.filter(name='add_value')
def add_value(field, value):
    """Add initial value to a form field"""
    if hasattr(field.field.widget, 'input_type') and field.field.widget.input_type in ['text', 'email', 'url', 'number']:
        field.field.widget.attrs['value'] = value
        field.field.widget.attrs['placeholder'] = f"Current: {value}"
    elif isinstance(field.field.widget, (forms.Textarea, forms.Select)):
        field.field.initial = value
        if isinstance(field.field.widget, forms.Textarea):
            field.field.widget.attrs['placeholder'] = "Current value:\n" + str(value)
    return field
