from django.contrib import admin

from django_summernote.admin import SummernoteModelAdmin
from .models_questions import Question, QuestionComment, Answer

class AnswerInline(admin.StackedInline):
	model = Answer
	extra = 1

class QuestionAdmin(SummernoteModelAdmin):
	list_display = ('name', 'email', 'status', 'created_on')
	list_filter = ('status', 'created_on', 'answer')
	search_fields = ['name', 'email', 'content']
	actions = ['publish_questions', 'draft_questions']

	inlines = [AnswerInline]
	summernote_fields = ('content')

	def publish_questions(self, request, queryset):
		queryset.update(status=1)
	
	def draft_questions(self, request, queryset):
		queryset.update(status=0)

class QuestionCommentAdmin(SummernoteModelAdmin):
	list_display = ('name', 'question', 'created_on', 'active')
	list_filter = ('active', 'created_on')
	search_fields = ('name', 'email', 'body')
	actions = ['approve_comments', 'disapprove_comments']
	
	summernote_fields = ('body', )
	def approve_comments(self, request, queryset):
		queryset.update(active=True)
	
	def disapprove_comments(self, request, queryset):
		queryset.update(active=False)
