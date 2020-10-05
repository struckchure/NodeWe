from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse

from . import models
from . import forms
from . import utils


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

# External context

def external_context(request=None):
	courses = models.Course.objects.all().order_by('-popularity', '-views', '-last_updated')
	categories = models.Category.objects.all().order_by('-popularity', '-last_updated')
	tutors = get_user_model().objects.filter(is_tutor=True, is_active=True)

	cart = None
	user = None

	if request.user.is_authenticated:
		user = request.user
		cart, created = models.Cart.objects.get_or_create(user=user)

	context = {
		'user': user,
		'cart': cart,
		'courses': courses,
		'categories': categories,
		'tutors': tutors,
		'all_courses_header': 'Courses'
	}

	return context


# Default view format

def Default(request):
	request.session['next'] = request.path
	
	template_name = 'default.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


# Authentification


def signUp(request):
	template_name = 'register.html'
	context = {

	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	if request.method == 'POST':
		signUpForm = forms.SignUpForm(request.POST)
		if signUpForm.is_valid():
			signUpForm.save()

			return redirect('Home:login')
		else:
			return redirect('Home:register')

	return render(request, template_name, context)


def signIn(request):
	template_name = 'login.html'
	context = {

	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	if request.method == 'POST':
		signInForm = forms.SignInForm(request.POST)
		if signInForm.is_valid():
			username = signInForm.cleaned_data.get('username')
			password = signInForm.cleaned_data.get('password')

			user = authenticate(
				username=username,
				password=password
			)

			if user:
				login(request, user)
				
				message = 'Login successful !'
				messages.info(request, message)
				
				return redirect('Home:index')
			else:
				message = 'Incorrect Username or Password'
				messages.warning(request, message)

				return redirect('Home:login')
	else:
		signInForm = forms.SignInForm()

	return render(request, template_name, context)


# Mains


def IndexView(request):
	template_name = 'Home/index.html'
	context = {
		
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def cartView(request):
	request.session['next'] = request.path

	template_name = 'cart.html'
	context = {
		
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def addToCart(request, slug):
	next_url = request.session['next']

	item = get_object_or_404(models.Course, slug=slug)
	cart =  get_object_or_404(models.Cart, user=request.user)

	new_cart_item, created = models.CartItem.objects.get_or_create(
		cart=cart,
		item=item
	)

	new_cart_item.save()

	if not next_url:
		next_url = item.get_absolute_url()

	# next_url = request.path

	return redirect(next_url)


def userCourses(request):
	request.session['next'] = request.path

	if request.user.is_tutor:
		courses = models.Course.objects.filter(tutor=request.user).order_by('-popularity', '-views', '-last_updated')
		categories = models.Category.objects.all().order_by('-popularity', '-last_updated')
	else:
		courses = models.Course.objects.filter().order_by('-popularity', '-views', '-last_updated')
		categories = models.Category.objects.all().order_by('-popularity', '-last_updated')

	template_name = 'Home/allCategories.html'
	context = {
		'all_courses_header': 'My Courses',
		'courses': courses,
		'categories': categories
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def categories(request):
	request.session['next'] = request.path

	like = models.CourseLike.objects.all().filter(user=request.user)

	template_name = 'Home/category.html'
	context = {
		'like': like,
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def allCategories(request):
	request.session['next'] = request.path

	template_name = 'Home/allCategories.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def categoryDetails(request, slug):
	request.session['next'] = request.path

	category = get_object_or_404(models.Category, slug=slug)

	template_name = 'Home/categoryDetails.html'
	context = {
		'category': category
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def courses(request):
	request.session['next'] = request.path

	template_name = 'Home/allCategories.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def courseDetails(request, slug):
	request.session['next'] = request.path

	course = get_object_or_404(models.Course, slug=slug)

	template_name = 'Home/product.html'
	context = {
		'course': course,
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required(login_url='Home:signIn')
def dashBoard(request):
	request.session['next'] = request.path

	user = models.User.objects.get(pk=request.user.id)

	template_name = 'dashboard.html'
	context = {
		'user': user
	}

	return render(request, template_name, context)


def CourseListView(request, slug):
	request.session['next'] = request.path

	course = models.Course.objects.get(slug=slug)
	videos = models.CourseItem.objects.all().filter(course=course)

	template_name = 'Home/courseList.html'
	context = {
		'videos': videos,
		'course': course
	}

	return render(request, template_name, context)


def likeCategory(request, slug):
	next_url = request.session['next']

	category = models.Category.objects.get(slug=slug)
	user_like = models.CategoryLike.objects.get_or_create(
		user=models.User.objects.get(pk=request.user.id),
		category=category
	)

	if user_like[0].status:
		category.popularity -= 1
		user_like[0].status = False
	else:
		category.popularity += 1
		user_like[0].status = True

	user_like[0].save()
	category.save()

	return redirect(next_url)


def likeCourse(request, slug):
	next_url = request.session['next']

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

	return redirect(next_url)
