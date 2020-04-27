from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from .models_posts import Post, PostComment



class PostAdmin(SummernoteModelAdmin):
	list_display = ('title', 'slug', 'status', 'created_on')
	list_filter = ('status', 'created_on')
	search_fields = ['title', 'content']
	prepopulated_fields = {'slug': ('title',)}
	actions = ['publish_posts']

	summernote_fields = ('content')

	def publish_posts(self, request, queryset):
		queryset.update(status=1)

class PostCommentAdmin(SummernoteModelAdmin):
	list_display = ('name', 'post', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments', 'disapprove_comments']
	
	summernote_fields = ('body', )
	def approve_comments(self, request, queryset):
		queryset.update(active=True)
	
	def disapprove_comments(self, request, queryset):
		queryset.update(active=False)
