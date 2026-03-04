from django import template

register = template.Library()

@register.filter(name='range_filter')
def range_filter(value):
    try:
        return range(int(value))
    except ValueError:
        return range(0) 
