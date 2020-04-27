from django.contrib import admin

from .models_questions import Question, QuestionComment, Answer

# Register your models here.
class QuestionCommentInline(admin.TabularInline):
	model = QuestionComment
	extra = 1

class AnswerInline(admin.StackedInline):
	model = Answer
	extra = 1

class QuestionAdmin(admin.ModelAdmin):
	inlines = [AnswerInline, QuestionCommentInline]
	list_filter = ['question_date']
	list_display = ('question_by', 'category', 'question_date')
	search_fields = ['question_text', 'category', 'question_by']

admin.site.register(Question, QuestionAdmin)
