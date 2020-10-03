from django.urls import path

from . import views


app_name = 'Home'


urlpatterns = [
	# Account & AUTHs

	path('', views.IndexView, name='index'),
	path('account/', views.dashBoard, name='dashboard'),
	path('account/login/', views.signIn, name='login'),
	path('account/register/', views.signUp, name='register'),

	# Categories

	path('categories/', views.categories, name='categories'),
	path('categories/<slug:slug>/', views.categoriesDetails, name='categoryDetails'),
	path('categories/<slug:slug>/like/', views.likeCategory, name='likeCategory'),

	# Courses / Products
	path('categories/courses/', views.courses, name='courses'),
	path('categories/courses/<slug:slug>/', views.courseDetails, name='courseDetails'),
	# Like Course
	path('categories/courses/<slug:slug>/like/', views.likeCourse, name='likeCourse'),
]
