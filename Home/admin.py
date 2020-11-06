from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
	fields = (
		'first_name',
		'last_name',
		'username',
		'email',
		'user_permissions',
		'groups',
		'last_login',
		'is_superuser',
		'is_active',
		'is_staff',
		'is_student',
		'is_tutor'
	)
	list_display = ('username', 'email', 'date', 'user_permissions')
	search_fields = ('first_name', 'last_name', 'username', 'email')


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category', 'description',)
	search_fields = ('category', 'description',)


class CourseAdmin(admin.ModelAdmin):
	list_display = ('category', 'description', 'date', 'last_updated')
	search_fields = ('category', 'description',)
	fieldsets = (
	    ('New Course', {
	        'fields': ('tutor', 'category', 'course', 'description', 'image', 'price')
	    	}
	    ),
	    ('Ratings', {
	    	'fields': ('popularity', 'views',)
	    	}
	    )
	)

class CourseItemAdmin(admin.ModelAdmin):
	list_display = ('course', 'title', 'description', 'file')


admin.site.register(models.User, UserAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Section)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseItem, CourseItemAdmin)
