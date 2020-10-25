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


def download_file(request, path):
	file_path = os.path.join(settings.MEDIA_ROOT, path)
	
	if os.path.exists(file_path):
		with open(file_path, 'rb') as fh:
			response = HttpResponse(fh.read(), content_type="application/download")
			response['Content-Disposition'] = "inline; filename=%s" % os.path.basename(file_path)

			return response

	raise Http404

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
	sections = models.Section.objects.order_by('-popularity', '-views', '-last_updated')
	courses = models.Course.objects.order_by('-popularity', '-views', '-last_updated')
	categories = models.Category.objects.all().order_by('-popularity', '-last_updated')
	tutors = User.objects.filter(is_tutor=True, is_active=True)

	cart = None
	user = None
	messages = None

	if request.user.is_authenticated:
		user = request.user
		cart, created = models.Cart.objects.get_or_create(user=user)
		messages = models.Message.objects.filter(recipient=request.user)

	context = {
		'request': request,
		'user': user,
		'cart': cart,
		'inbox': messages,
		'sections': sections,
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
	request.session['next'] = request.path

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

			# username = signUpForm.cleaned_data.get('username')
			# password = signUpForm.cleaned_data.get('password')

			# user = authenticate(username=username, password=password)
			# login(request, user)

			return redirect('Home:dashboard')

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

	if request.user == user:
		messages.success(request, 'Account is not verified :)')
		user.verify_user()
		token.delete()
	else:
		print('Not user')


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
def dashboardCourseDetail(request, slug):
	request.session['next'] = request.path

	course = get_object_or_404(models.Course, slug=slug)

	template_name = 'Home/dashboardCourseDetail.html'
	context = {
		'course': course
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

	mail_compose_form = forms.ComposeMail(request.POST, request.FILES)
	sender = request.user

	if mail_compose_form.is_valid():
		recipient = User.objects.filter(
			username=mail_compose_form.cleaned_data.get('recipient')
		)
		subject = mail_compose_form.cleaned_data.get('subject')
		attachments = mail_compose_form.cleaned_data.get('attachment')

		if recipient.exists():
			recipient = recipient[0]
			message = mail_compose_form.cleaned_data.get('message')

			mail = models.Message.objects.create(
				sender=sender,
				recipient=recipient,
				subject=subject,
				message=message,
				attachment=attachments if attachments else None
			)

			mail.save()
		else:
			print('username does not exist')
	else:
		print('invalid form')

	template_name = 'Home/mailboxCompose.html'
	context = {
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


# class mailboxCompose(View):
#     def get(self, request):
#     	template_name = 'Home/mailboxCompose.html'
#     	context = utils.dictMerge(external_context(self.request), {})

#     	return render(self.request, template_name, context)

#     def post(self, request):
#         mail_compose_form = forms.ComposeMail(self.request.POST, self.request.FILES)
#         sender = self.request.user

#         if mail_compose_form.is_valid():
#         	recipient = User.objects.filter(username=mail_compose_form.cleaned_data.get('recipient'))
#         	subject = mail_compose_form.cleaned_data.get('subject')
#         	attachments = mail_compose_form.cleaned_data.get('attachment')
#         	data = {'is_valid': True, 'name': attachments.file.name, 'url': attachments.file.url}

#         	if recipient.exists():
#         		recipient = recipient[0]
#         		message = mail_compose_form.cleaned_data.get('message')
#         		mail = models.Message.objects.create(
# 					sender=sender,
# 					recipient=recipient,
# 					subject=subject,
# 					message=message,
# 					attachment=attachments if attachments else None
# 				);mail.save()
#         	else:
#         		print('username does not exist')
#         	return JsonResponse(data)
#         else:
#         	data = {'is_valid': False}

#         	return JsonResponse(data)


@login_required
def mailboxTrash(request):
	request.session['next'] = request.path

	messages = models.Message.objects.filter(sender=request.user, trashed=True)

	template_name = 'Home/mailbox.html'
	context = {
		'inbox': messages,
	}
	context = utils.dictMerge(
		external_context(request),
		context
	)

	return render(request, template_name, context)


@login_required
def mailboxSent(request):
	request.session['next'] = request.path

	messages = models.Message.objects.filter(sender=request.user, trashed=False)

	template_name = 'Home/mailbox.html'
	context = {
		'inbox': messages,
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

	template_name = 'Home/product.html'
	context = {
		'course': course,
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
