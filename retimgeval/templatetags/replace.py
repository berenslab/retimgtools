from django import template

register = template.Library()


@register.filter(name="replace")
def replace(value, arg):
    old_val, new_val = arg.split(",")
    return value.replace(old_val, new_val)
