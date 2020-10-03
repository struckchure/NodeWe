'''
	Utitlities
'''


def dictMerge(*args):
	dictionary = {}
	for i in args:
		dictionary = {**dictionary, **i}

	return dictionary
