from django import template

register = template.Library()

@register.filter(name="multipy")
def multipy(value,arg):
	return value * arg