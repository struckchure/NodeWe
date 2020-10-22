from django.urls import path, include

from . import views
from . import utils


app_name = 'Home'


urlpatterns = [
	# Account & AUTHs

	path('', views.IndexView, name='index'),
	path('account/', views.dashBoard, name='dashboard'),
	path('account/profile/<slug:slug>/', views.profile, name='profile'),
	path('account/login/', views.signIn, name='login'),
	path('account/register/', views.signUp, name='register'),
	path('account/logout/', views.signOut, name='logout'),

	# Mailbox

	path('account/mailbox/', views.mailbox, name='mailbox'),
	path('account/mailbox/new/', views.mailboxCompose, name='mailboxCompose'),
	path('account/mailbox/<slug:slug>/details/', views.mailboxDetail, name='mailboxDetail'),
	path('account/mailbox/trash/', views.mailboxTrash, name='mailboxTrash'),
	path('account/mailbox/sent/', views.mailboxSent, name='mailboxSent'),

	# Courses

	path('account/courses/materials/', views.dashboardMaterials, name='dashboardMaterials'),
	path('account/courses/', views.dashboardCourses, name='dashboardCourses'),
	path('account/courses/<slug:slug>/', views.dashboardCourseDetail, name='dashboardCourseDetail'),
	
	# Cart

	path('account/cart/', views.cartView, name='cartView'),
	path('account/cart/add/<slug:slug>/', views.addToCart, name='addToCart'),
	path('account/billings/', views.dashboardBillings, name='dashboardBillings'),
	path('account/cart/checkout', views.checkout, name='checkout'),

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

	# Utilities

	path('download/<slug:slug>/', views.download_file, name='downloadFile'),
]
