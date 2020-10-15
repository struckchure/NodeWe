from django import template

register = template.Library()


@register.filter(name='course_length')
def course_length(courses):
	length = 2
	
	return courses[:length]
