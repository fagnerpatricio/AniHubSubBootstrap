from django import template

register = template.Library()

@register.filter(is_safe=True)
def ler_id(value):
    return value['_id']
    # return value.lower()