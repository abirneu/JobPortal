from django import template

register = template.Library()

@register.filter
def filter_status(applications, status):
    return applications.filter(status=status)
