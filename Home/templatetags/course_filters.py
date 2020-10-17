from django import template

register = template.Library()


@register.filter
def course_length(courses):
	length = 2
	
	return courses[:length]
