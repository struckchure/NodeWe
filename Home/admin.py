from django.contrib import admin

from . import models


class UserAdmin(admin.ModelAdmin):
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
