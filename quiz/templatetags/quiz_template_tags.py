from django import template

register = template.Library()

@register.filter
def modulo(num, val):
    return num % val

@register.filter
def multiply(num, val):
    return int(num) * int(val)

@register.filter
def div(num, val):
    return int(num) / int(val)
