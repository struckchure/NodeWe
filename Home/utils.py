import mimetypes
import os
from django.conf import settings
from django.http import HttpResponse, Http404

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

	file_path = f'Sections/{section}/{category}/courses/{course}/{title}.{file_extension}'.replace(' ', '-')

	return file_path

def course_cover_upload_handler(instance, filename):
	file_extension = str(instance.image).split('.')[-1]
	course = instance.course

	file_path = f'Images/courses/{course}.{file_extension}'.replace(' ', '-')

	return file_path

def course_item_cover_upload_handler(instance, filename):
	file_extension = str(instance.cover).split('.')[-1]
	item = instance.title

	file_path = f'Images/courses/item cover-{item}.{file_extension}'.replace(' ', '-')

	return file_path


def category_cover_upload_handler(instance, filename):
	file_extension = str(instance.image).split('.')[-1]
	category = instance.category

	file_path = f'Images/category/{category}.{file_extension}'.replace(' ', '-')

	return file_path

def profile_upload_handler(instance, filename):
	file_extension = str(instance.avatar).split('.')[-1]
	username = instance.user.username

	file_path = f'Images/users/{username}.{file_extension}'.replace(' ', '-')

	return file_path


def message_upload_handler(instance, filename):
	file_extension = str(instance.attachment).split('.')[-1]
	attachment = instance.attachment
	
	file_path = f'Messages/attachment/{attachment}.{file_extension}'.replace(' ', '-')

	return file_path


def download_file(request, slug):
	item = get_object_or_404(models.CourseItem, slug=slug)
	filename = item.file.path

	fl_path = filename
	fl = open(fl_path, 'r')
	mime_type, _ = mimetypes.guess_type(fl_path)
	response = HttpResponse(fl, content_type=mime_type)
	response['Content-Disposition'] = "attachment; filename=%s" % filename

	return response


# def download_file(request, path):
#     file_path = path

#     if os.path.exists(file_path):
#         with open(file_path, 'rb') as fh:
#             response = HttpResponse(fh.read(), content_type="application/vnd.ms-excel")
#             response['Content-Disposition'] = 'inline; filename=' + os.path.basename(file_path)
            
#             return response

#     raise Http404

def handle_uploaded_file(f):
    with open('some/file/name.txt', 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)