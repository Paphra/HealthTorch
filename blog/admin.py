from django.contrib import admin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin

from .models_posts import Post, PostComment
from .models import Category, ImageGroup, Profile, Image, Subscriber, About


class ProfileInline(admin.StackedInline):
	model = Profile

class UserAdmin(admin.ModelAdmin):
	inlines = [ProfileInline]
	list_display = (
		'username', "first_name", 'last_name', 'date_joined')
	search_fields = [
		'username', 'first_name', 'last_name', 'email']
	list_filter = ['date_joined']

class ImageInline(admin.TabularInline):
	model = Image
	exclude = ['data', 'description']

class ImageGroupAdmin(admin.ModelAdmin):
	inlines = [ImageInline]

class CategoryAdmin(admin.ModelAdmin):
	verbose_name = 'Categories'
	class Meta:
		verbose_name_plural = "Categories"

admin.site.unregister(User)
admin.site.register(User, UserAdmin)

admin.site.register(ImageGroup, ImageGroupAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Subscriber)

admin.site.register(About)

from .admin_posts import PostAdmin, PostCommentAdmin

admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)
