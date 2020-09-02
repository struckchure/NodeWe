from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.shortcuts import redirect

from . import models
from . import forms

# Errors

def Error404(request, exception=None):
	template_name = 'Error404.html'
	
	return render(request, template_name)


def Error400(request, exception=None):
	template_name = 'Error400.html'

	return render(request, template_name)


def Error403(request, exception=None):
	template_name = 'Error403.html'
	
	return render(request, template_name)


def Error500(request, exception=None):
	template_name = 'Error500.html'
	
	return render(request, template_name)


# Authentification


def signUp(request):
	template_name = 'signUp.html'
	context = {

	}

	return render(request, template_name, context)


def signIn(request):
	template_name = 'signIn.html'
	context = {

	}

	if request.method == 'POST':
		signInForm = forms.SignInForm(request.POST)
		if signInForm.is_valid():
			username = signInForm.cleaned_data.get('username')
			password = signInForm.cleaned_data.get('password')
			print(username, password)
			user = authenticate(
				username=username,
				password=password
			)

			if user:
				login(request, user)
				
				message = 'Login successful !'
				messages.info(request, message)
				
				return redirect('Home:dashboard')
			else:
				message = 'Incorrect Username or Password'
				messages.warning(request, message)

				return redirect('Home:signIn')
	else:
		signInForm = forms.SignInForm()

	return render(request, template_name, context)


# Mains


def IndexView(request):
	courses = models.Course.objects.all().order_by('-popularity', '-views', '-last_updated')

	template_name = 'Home/index.html'
	context = {
		'courses': courses
	}

	return render(request, template_name, context)


def categories(request):
	categories = models.Category.objects.all().order_by('-popularity', '-views', '-last_updated')

	template_name = 'Home/categories.html'
	context = {
		'categories': categories
	}

	return render(request, template_name, context)


def CategoryListView(request, slug):
	category = models.Category.objects.get(slug=slug)
	courses = models.Course.objects.all().filter(category=category)

	template_name = 'Home/categoryList.html'
	context = {
		'category': category,
		'courses': courses
	}

	return render(request, template_name, context)


@login_required(login_url='Home:signIn')
def dashBoard(request):
	user = models.User.objects.get(pk=request.user.id)

	template_name = 'dashboard.html'
	context = {
		'user': user
	}

	return render(request, template_name, context)


def CourseListView(request, slug):
	course = models.Course.objects.get(slug=slug)
	videos = models.CourseItem.objects.all().filter(course=course)

	template_name = 'Home/courseList.html'
	context = {
		'videos': videos,
		'course': course
	}

	return render(request, template_name, context)


def likeCategory(request, slug):
	category = models.Category.objects.get(slug=slug)
	user_like = models.CategoryLike.objects.get_or_create(pk=request.user.id)

	if user_like.status:
		category.popularity -= 1
		user_like.status = False
	else:
		category.popularity += 1
		user_like.status = True

	user_like.save()
	category.save()

	return redirect('Home:index')


def likeCourse(request, slug):
	course = models.Course.objects.get(slug=slug)
	user_like = models.CourseLike.objects.get_or_create(
		user=models.User.objects.get(pk=request.user.id),
		course=course
	)

	if user_like[0].status:
		course.popularity -= 1
		user_like[0].status = False
	else:
		course.popularity += 1
		user_like[0].status = True

	user_like[0].save()
	course.save()

	return redirect('Home:index')
