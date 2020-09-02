from django.urls import path

from . import views


app_name = 'Home'


urlpatterns = [
	path('', views.IndexView, name='index'),
	path('account/', views.dashBoard, name='dashboard'),
	path('account/signin/', views.signIn, name='signIn'),
	path('account/signup/', views.signUp, name='signUp'),
	path('courses/', views.IndexView, name='courses'),
	path('courses/<slug:slug>/', views.CourseListView, name='courseList'),
	path('courses/<slug:slug>/like/', views.likeCourse, name='likeCourse'),
	path('categories/', views.categories, name='categories'),
	path('categories/<slug:slug>/', views.CategoryListView, name='categoryList'),
	path('categories/<slug:slug>/like/', views.likeCategory, name='likeCategory'),
]
