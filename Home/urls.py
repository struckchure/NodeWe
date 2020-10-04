from django.urls import path

from . import views


app_name = 'Home'


urlpatterns = [
	# Account & AUTHs

	path('', views.IndexView, name='index'),
	path('account/', views.dashBoard, name='dashboard'),
	path('account/login/', views.signIn, name='login'),
	path('account/register/', views.signUp, name='register'),
	path('account/cart', views.cartView, name='cartView'),

	# Categories

	path('categories/', views.categories, name='categories'),
	path('categories/all', views.allCategories, name='allCategories'),
	path('categories/<slug:slug>/', views.categoryDetails, name='categoryDetails'),
	path('categories/<slug:slug>/like/', views.likeCategory, name='likeCategory'),

	# Courses / Products
	path('categories/courses/all', views.courses, name='courses'),
	path('categories/courses/<slug:slug>/', views.courseDetails, name='courseDetails'),
	# Like Course
	path('categories/courses/<slug:slug>/like/', views.likeCourse, name='likeCourse'),
]
