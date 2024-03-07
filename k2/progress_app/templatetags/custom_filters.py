from django import template

register = template.Library()

@register.filter(name='multiply_and_format_percentage')
def multiply_and_format_percentage(value):
    ans=value * 100
    return f"{ans:.2f}"
