from django.shortcuts import render
from django.views import generic
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.shortcuts import redirect, get_object_or_404
from django.urls import reverse
from django.conf import settings
from django.views.static import serve
from django.views import View
from django.http import FileResponse, HttpResponse, Http404, JsonResponse
import os

from . import models
from . import forms
from . import utils

# Utils


User = get_user_model()


# Errors

def Error404(request, exception=None):
	template_name = 'ErrorPages/Error404.html'
	
	return render(request, template_name)


def Error400(request, exception=None):
	template_name = 'ErrorPages/Error400.html'

	return render(request, template_name)


def Error403(request, exception=None):
	template_name = 'ErrorPages/Error403.html'
	
	return render(request, template_name)


def Error500(request, exception=None):
	template_name = 'ErrorPages/Error500.html'
	
	return render(request, template_name)

# External context

def external_context(request=None):
	sections = models.Section.objects.order_by('-popularity', '-views', '-last_updated')
	courses = models.Course.objects.order_by('-popularity', '-views', '-last_updated')
	viewed_courses = models.Course.objects.order_by('-views')
	populary_courses = models.Course.objects.order_by('-popularity')
	user_suggested_courses = models.Course.objects.all()
	categories = models.Category.objects.all().order_by('-popularity', '-last_updated')
	tutors = User.objects.filter(is_tutor=True, is_active=True)

	cart = None
	user = None
	inbox = None
	sent = None

	if request.user.is_authenticated:
		user = request.user
		cart, created = models.Cart.objects.get_or_create(user=user)
		inbox = models.Message.objects.filter(recipient=request.user).order_by('-date')
		sent = models.Message.objects.filter(sender=request.user).order_by('-date')

	context = {
		'request': request,
		'user': user,
		'cart': cart,
		'inbox': inbox,
		'inbox_count': inbox.count() if inbox else 0,
		'sent_count': sent.count() if sent else 0,
		'sections': sections,
		'courses': courses,
		'viewed_courses': viewed_courses,
		'populary_courses': populary_courses,
		'user_suggested_courses': user_suggested_courses,
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
	if request.method == 'POST':
		signUpForm = forms.SignUpForm(request.POST)
		if signUpForm.is_valid():
			username = signUpForm.cleaned_data.get('username')
			email = signUpForm.cleaned_data.get('email')
			password1 = signUpForm.cleaned_data.get('password1')
			password2 = signUpForm.cleaned_data.get('password2')

			emails = User.objects.values_list('email', flat=True)

			if email not in emails:
				if password1 == password2:
					new_user = User.objects.create(
						username=username,
						email=email
					)
					new_user.set_password(password1)
					new_user.save()

					messages.info(request, 'Registration complete, check your Mail to verify your account')

					username = signUpForm.cleaned_data.get('username')
					password = password1

					user = authenticate(username=username, password=password)
					token = models.VerificationToken.objects.get(user=user)
					token.user.send_verification(token.token)

					if user:
						login(request, user)

					return redirect('Home:dashboard')
				else:
					messages.info(request, 'Password mismatch')
			else:
				messages.info(request, 'Email already exist')
	else:
		signUpForm = forms.SignUpForm()

	template_name = 'register.html'
	context = {
		'signup_form': signUpForm
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


def signIn(request):
	request.session['next'] = request.path

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
				
				return redirect('Home:dashboard')
			else:
				message = 'Incorrect Username or Password'
				messages.warning(request, message)

				return redirect('Home:login')
	else:
		signInForm = forms.SignInForm()

	return render(request, template_name, context)


def signOut(request):
	logout(request)

	return redirect('Home:dashboard')


# Accounts

@login_required
def verify(request, token):
	token = get_object_or_404(models.VerificationToken, token=token)
	user = token.user

	messages.success(request, 'Account is not verified :)')
	user.verify_user()
	token.delete()

	login(request, user)

	return redirect('Home:dashboard')


@login_required
def dashBoard(request):
	request.session['next'] = request.path

	template_name = 'Home/dashboard.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def dashboardCourses(request):
	request.session['next'] = request.path

	template_name = 'Home/dashboardCourses.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def dashboardCourseDetail(request, slug, material=False):
	request.session['next'] = request.path

	course = get_object_or_404(models.Course, slug=slug)
	material_course = models.CourseItem.objects.filter(slug=material).exists()
	if not material_course:
		material_course = False
	else:
		material_course = models.CourseItem.objects.get(slug=material)

	if request.method == 'POST':
		comment_form = forms.CommentForm(request.POST)
		if comment_form.is_valid():
			comment = comment_form.cleaned_data.get('comment')

			new_comment = models.Comment.objects.create(
				user=request.user,
				course=course,
				comment=comment
			)

			new_comment.save()

			messages.info(request, 'Your comment has been sent')
	else:
		comment_form = forms.CommentForm()

	template_name = 'Home/dashboardCourseDetail.html'
	context = {
		'course': course,
		'material': material_course,
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def dashboardBillings(request):
	request.session['next'] = request.path

	template_name = 'Home/dashboardBillings.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def dashboardMaterials(request):
	request.session['next'] = request.path

	template_name = 'Home/dashboardMaterials.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def profile(request, slug=None):
	user = get_object_or_404(get_user_model(), username=slug)

	request.session['next'] = request.path

	template_name = 'Home/profile.html'
	context = {
		'userProfile': user
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def mailbox(request):
	request.session['next'] = request.path

	template_name = 'Home/mailbox.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def mailboxDetail(request, slug):
	request.session['next'] = request.path

	mail = get_object_or_404(models.Message, slug=slug)

	template_name = 'Home/mailboxDetail.html'
	context = {
		'mail': mail
	}
	
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def mailboxCompose(request):
	request.session['next'] = request.path

	sender = request.user

	if request.method == 'POST':
		mail_compose_form = forms.ComposeMail(request.POST, request.FILES)
		if mail_compose_form.is_valid():
			recipient = mail_compose_form.cleaned_data.get('recipient')
			recipient = User.objects.get(
				username=recipient
			) if recipient in models.User.objects.all().values_list('username', flat=True) else None

			subject = mail_compose_form.cleaned_data.get('subject')
			attachments = mail_compose_form.cleaned_data.get('attachment')

			if recipient:
				message = mail_compose_form.cleaned_data.get('message')

				mail = models.Message.objects.create(
					sender=sender,
					recipient=recipient,
					subject=subject,
					message=message,
					attachment=attachments if attachments else None
				)

				mail.save()

				messages.info(request, 'Mail sent !!!')
			else:
				messages.info(request, 'Username does not exist')
		else:
			print('invalid form')
	else:
		mail_compose_form = forms.ComposeMail()

	template_name = 'Home/mailboxCompose.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def mailboxTrash(request):
	request.session['next'] = request.path

	template_name = 'Home/mailbox.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def mailboxSent(request):
	request.session['next'] = request.path

	sent = models.Message.objects.filter(sender=request.user).order_by('-date')

	template_name = 'Home/mailboxSent.html'
	context = {
		'inbox': sent
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


# Mains


def IndexView(request):
	request.session['next'] = request.path

	template_name = 'Home/index.html'
	context = {
		
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
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


@login_required
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


@login_required
def checkout(request):
	template_name = 'checkout.html'
	context = {}
	context = context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


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
	related_courses = models.Course.objects.filter(category=course.category)
	reviews = course.popularity

	template_name = 'Home/product.html'
	context = {
		'course': course,
		'related_courses': related_courses,
		'reviews': reviews,
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

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

	if request.user.is_authenticated:
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
