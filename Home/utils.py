'''
	Utitlities
'''


def dictMerge(*args):
	dictionary = {}
	for i in args:
		dictionary = {**dictionary, **i}

	return dictionary

def course_upload_handler(instance, filename):
	file_extension = str(instance.file).split('.')[-1]
	file = instance.file
	title = instance.title
	course = instance.course.course
	category = instance.course.category
	section = instance.course.category.section.section

	file_path = f'Sections/{section}/{category}/courses/{course}/{title}.{file_extension}'

	return file_path

def course_cover_upload_handler(instance, filename):
	file_extension = str(instance.image).split('.')[-1]
	course = instance.course

	file_path = f'Images/courses/{course}.{file_extension}'

	return file_path


def category_cover_upload_handler(instance, filename):
	file_extension = str(instance.image).split('.')[-1]
	category = instance.category

	file_path = f'Images/category/{category}.{file_extension}'

	return file_path

def profile_upload_handler(instance, filename):
	file_extension = str(instance.avatar).split('.')[-1]
	username = instance.username

	file_path = f'Images/users/{username}.{file_extension}'

	return file_path


def message_upload_handler(instance, filename):
	file_extension = str(instance.attachment).split('.')[-1]
	date = instance.date
	
	file_path = f'Messages/attachment/{date}.{file_extension}'

	return file_path