from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
	fields = (
		'first_name',
		'last_name',
		'username',
		'email',
		'is_active',
		'is_staff',
		'is_student',
		'is_tutor'
	)
	list_display = ('first_name', 'last_name', 'username')
	search_fields = ('first_name', 'last_name', 'username', 'email')


class ProfileAdmin(admin.ModelAdmin):
	list_display = ('user', 'avatar',)


class CategoryAdmin(admin.ModelAdmin):
	list_display = ('category', 'description',)
	search_fields = ('category', 'description',)



class CourseAdmin(admin.ModelAdmin):
	list_display = ('category', 'description',)
	search_fields = ('category', 'description',)
	fieldsets = (
	    ('New Course', {
	        'fields': ('category', 'course', 'description', 'image',)
	    	}
	    ),
	    # ('Ratings', {
	    # 	'fields': ('popularity', 'views',)
	    # 	}
	    # )
	)

class CourseItemAdmin(admin.ModelAdmin):
	list_display = ('course', 'title', 'description', 'file')


admin.site.register(models.User)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseItem, CourseItemAdmin)
