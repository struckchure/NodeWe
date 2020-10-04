from django.db import models
from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin
from django.urls import reverse
from django.utils.text import slugify
from django.utils import timezone
import os
import random

from . import managers
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

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'


class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	avatar = models.FileField(blank=True, upload_to='Images/')
	date = models.DateTimeField(auto_now=True)
	last_updated = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return f'{self.user.username}'

	class Meta:
		verbose_name = 'Profile'
		verbose_name_plural = 'Profiles'


class Category(models.Model):
	category = models.CharField(max_length=100, blank=False, unique=True)
	image = models.FileField(upload_to='Images/', blank=True)
	description = models.TextField()
	popularity = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
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

	class Meta:
		verbose_name = 'Category'
		verbose_name_plural = 'Categories'


class Course(models.Model):
	category = models.ForeignKey(Category, on_delete=models.CASCADE)
	course = models.CharField(max_length=200, blank=False)
	image = models.FileField(upload_to='Images/', blank=True, default='default_avatar')
	description = models.TextField(blank=False)
	popularity = models.IntegerField(default=0)
	views = models.IntegerField(default=0)
	date = models.DateTimeField(auto_now=True)
	last_updated = models.DateTimeField(auto_now_add=True)
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
		self.slug = self.custom_slugify(f'{self.course}')
		super(Course, self).save(*args, **kwargs)

	def get_course(self):
		return self.course

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

	class Meta:
		verbose_name = 'Course'
		verbose_name_plural = 'Courses'


class CourseItem(models.Model):
	course = models.ForeignKey(Course, on_delete=models.CASCADE)
	title = models.CharField(max_length=200, blank=False, default='')
	description = models.TextField(blank=False)
	file = models.FileField(blank=False, upload_to='Videos/')

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
