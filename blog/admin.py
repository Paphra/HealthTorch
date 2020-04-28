from django.contrib import admin
from django.contrib.auth.models import User
from django_summernote.admin import SummernoteModelAdmin

from .models_posts import Post, PostComment
from .models_questions import Question, QuestionComment, Answer
from .models import Category, ImageGroup, Profile, Image, Subscriber, About, Partner


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

class AboutAdmin(SummernoteModelAdmin):
	summernote_fields = ('info',)

admin.site.register(About, AboutAdmin)

from .admin_posts import PostAdmin, PostCommentAdmin
admin.site.register(Post, PostAdmin)
admin.site.register(PostComment, PostCommentAdmin)

from .admin_questions import QuestionAdmin, QuestionCommentAdmin
admin.site.register(Question, QuestionAdmin)
admin.site.register(QuestionComment, QuestionCommentAdmin)

class PartnerAdmin(admin.ModelAdmin):
	list_display = ('name', 'email','phone', 'address', 'created_on')
	search_fields = ['name', 'email', 'phone']
	list_filter = ['created_on', 'active']

admin.site.register(Partner, PartnerAdmin)