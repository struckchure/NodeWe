from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import os
import random

from . import managers
from . import utils
from NodeWe import settings

# Generics

new_course_frame = timezone.timedelta(days=5)

# User Models


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    username = models.CharField(max_length=100, blank=False, unique=True)
    email = models.EmailField(blank=False)
    date = models.DateTimeField(auto_now=True)
    last_updated = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True, blank=True)
    is_student = models.BooleanField(default=False)
    is_tutor = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = managers.UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)
        
        user_profile = Profile.objects.get_or_create(
            user=User.objects.get(pk=self.id)
        )
        user_profile[0].save()

    def get_full_name(self):
        return f'{self.first_name} {self.last_name}'

    @property
    def _is_student(self):
        return self.is_student

    @property
    def _is_tutor(self):
        return self.is_tutor

    def __str__(self):
        return self.username

    def get_courses(self):
    	return reverse('Home:userCourses')

    def get_user_courses(self):
    	if self.is_tutor:
    		courses = Course.objects.filter(tutor=self.id)
    	else:
    		courses = Course.objects.all()

    	return courses

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.FileField(blank=True, upload_to=utils.profile_upload_handler)
	date = models.DateTimeField(auto_now=True)
	last_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}'

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'


class Section(models.Model):
	section = models.CharField(max_length=200, blank=False)
	popularity = models.PositiveIntegerField(default=0)
	views = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(auto_now=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(blank=True, unique=True)

	def __str__(self):
		return f'{self.section}'

	def custom_slugify(self, text):
	    sections = Section.objects.all().values('slug')
	    section_slugs = []

	    for i in sections:
	        section_slugs.append(i['slug'])

	    intial_slug = slugify(text)
	    unique_slug_key = random.randint(1, 1000)
	    final_slug = f'{intial_slug}-{unique_slug_key}'

	    while text in section_slugs:
	        unique_slug_key = random.randint(1, 1000)
	        final_slug = f'{intial_slug}-{unique_slug_key}'
	    
	    return final_slug

	def save(self, *args, **kwargs):
		self.slug = self.custom_slugify(f'{self.section}')

		super(Section, self).save(*args, **kwargs)

	def get_categories(self):
		categories = Category.objects.filter(section=self.id)

		return categories

	def get_absolute_url(self):
		url = ''

		# return reverse(url)

	class Meta:
		verbose_name = 'Section'
		verbose_name_plural = 'Sections'


class Category(models.Model):
	category = models.CharField(max_length=200, blank=False, unique=True)
	section = models.ForeignKey(Section, on_delete=models.CASCADE, null=True)
	image = models.FileField(upload_to=utils.category_cover_upload_handler, blank=True)
	description = models.TextField()
	popularity = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now=True)
	last_updated = models.DateTimeField(auto_now_add=True)
	slug = models.SlugField(blank=True, unique=True)

	def __str__(self):
		return self.category

	def custom_slugify(self, text):
	    categories = Category.objects.all().values('slug')
	    category_slugs = []

	    for i in categories:
	        category_slugs.append(i['slug'])

	    intial_slug = slugify(text)
	    unique_slug_key = random.randint(1, 1000)
	    final_slug = f'{intial_slug}-{unique_slug_key}'

	    while text in category_slugs:
	        unique_slug_key = random.randint(1, 1000)
	        final_slug = f'{intial_slug}-{unique_slug_key}'
	    
	    return final_slug

	def save(self, *args, **kwargs):
		self.slug = self.custom_slugify(f'{self.category}')

		super(Category, self).save(*args, **kwargs)

	def get_courses(self, index=3):
		courses = Course.objects.filter(category=self.id)[:index]

		return courses

	def get_all_courses(self):
		courses = Course.objects.filter(category=self.id)

		return courses

	def get_tutor_courses(self):
		courses = Course.objects.filter(category=self.id)

		return courses

	def get_absolute_url(self):
		return reverse('Home:categoryDetails', args=[self.slug])

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'


class Course(models.Model):
	tutor = models.ForeignKey(User, on_delete=models.DO_NOTHING, blank=True, null=True)
	category = models.ForeignKey(Category, on_delete=models.CASCADE, null=True, blank=True)
	course = models.CharField(max_length=200, blank=False)
	image = models.FileField(upload_to=utils.course_cover_upload_handler, blank=True, default='default_avatar')
	description = models.TextField(blank=False)
	popularity = models.IntegerField(default=0)
	price = models.PositiveIntegerField(default=0)
	views = models.ManyToManyField(User, related_name='views', blank=True)
	date = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)
	slug = models.SlugField(blank=True, unique=True)

	def __str__(self):
		return f'{self.category.category} {self.course}'

	def custom_slugify(self, text):
	    courses = Course.objects.all().values('slug')
	    course_slugs = []

	    for i in courses:
	        course_slugs.append(i['slug'])

	    intial_slug = slugify(text)
	    unique_slug_key = random.randint(1, 1000)
	    final_slug = f'{intial_slug}-{unique_slug_key}'

	    while text in course_slugs:
	        unique_slug_key = random.randint(1, 1000)
	        final_slug = f'{intial_slug}-{unique_slug_key}'
	    
	    return final_slug

	def save(self, *args, **kwargs):
		self.slug = self.custom_slugify(f'{self.category} {self.course}')

		super(Course, self).save(*args, **kwargs)

	def get_course(self):
		return self.course

	def get_views(self):
		views = self.views.all()

		return views

	def get_absolute_url(self):
		return reverse('Home:courseDetails', args=[self.slug])

	def like_item(self):
		return reverse('Home:likeCourse', args=[self.slug])

	def is_new(self):
		is_new_course_time = new_course_frame + self.date
		current_time = timezone.now()

		if is_new_course_time >= current_time:
			return True
		else:
			return False

	def get_user_likes(self):
		likes = CourseLike.objects.filter(course=self.id, status=True)
		users = []

		for like in likes:
			users.append(like.user.username)

		return users

	class Meta:
		verbose_name = 'Course'
		verbose_name_plural = 'Courses'


class CourseItem(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, blank=False, default='')
	description = models.TextField(blank=False)
	file = models.FileField(blank=False, upload_to=utils.course_upload_handler)

	def __str__(self):
		return f'{self.course.course} {self.title}'

	def save(self, *args, **kwargs):
		super(CourseItem, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Course Item'
		verbose_name_plural = 'Course Items'


class CategoryLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)


class CourseLike(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE)
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	status = models.BooleanField(default=False)

	def __str__(self):
		return f'{self.user}-_-{self.course}'


class Cart(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	total_items = models.PositiveIntegerField(default=0)
	total_amount = models.PositiveIntegerField(default=0)
	date = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.user}'

	def cart_items(self):
		cart_items = CartItem.objects.filter(cart=self.id)

		return cart_items

	def get_total_amount(self):
		cart_items = CartItem.objects.filter(cart=self.id)
		prices = []

		for i in cart_items:
			prices.append(i.item.price)

		amount = sum(prices)
		self.total_amount = amount

		super(Cart, self).save()

		return amount

	class Meta:
		verbose_name = 'Cart'
		verbose_name_plural = 'Carts'


class CartItem(models.Model):
	cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
	item = models.ForeignKey(Course, on_delete=models.DO_NOTHING)
	date = models.DateTimeField(auto_now_add=True)
	last_updated = models.DateTimeField(auto_now=True)

	def __str__(self):
		return f'{self.cart}-_-{self.item}'

	def save(self, *args, **kwargs):
		cart = Cart.objects.get(user=self.cart.user)
		
		try:
			item = CartItem.objects.get(cart=cart, item=self.item)
		except CartItem.DoesNotExist:
			cart.total_items += 1
			cart.total_amount += self.item.price

		cart.save()

		super(CartItem, self).save(*args, **kwargs)

	class Meta:
		verbose_name = 'Cart item'
		verbose_name_plural = 'Cart items'
