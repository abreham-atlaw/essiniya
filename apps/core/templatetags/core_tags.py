from django import template

import random

register = template.Library()

@register.simple_tag
def version():
	return random.randint(1,50)