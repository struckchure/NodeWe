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


class MessageAdmin(admin.ModelAdmin):
	fields = (
		'sender',
		'recipient',
		'subject',
		'attachment'
	)
	list_display = ('sender', 'recipient', 'subject', 'subject', 'attachment')
	search_fields = ('sender', 'recipient', 'subject', 'subject')


admin.site.register(models.User)
admin.site.register(models.Profile, ProfileAdmin)
admin.site.register(models.Category, CategoryAdmin)
admin.site.register(models.Section)
admin.site.register(models.Course, CourseAdmin)
admin.site.register(models.CourseItem, CourseItemAdmin)
admin.site.register(models.Cart)
admin.site.register(models.CartItem)
admin.site.register(models.Message, MessageAdmin)
admin.site.register(models.VerificationToken)
