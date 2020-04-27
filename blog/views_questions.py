import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator

from .models_questions import Question, QuestionComment, Answer
from .models import Category

# Create your views here.

def set_context(context, request, search=True):
	context['c_user'] = request.user
	context['atquestions'] = True
	context['search'] = search
	context['categories'] = Category.objects.all()

def index(request):
	template_name = "questions/index.html"
	questions = Question.objects.all().order_by('-question_date')
	context = {
		'questions': questions,
		'title': 'Questions'
	}
	
	paginator = Paginator(questions, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(context, request)
	return render(request, template_name, context)	

def ask(request):
	"""
	Allows asking a question
	"""
	template = "questions/ask.html"
	
	context = {
		'title': 'Ask A Question'
	}
	set_context(context, request, False)

	return render(request, template, context)

def detail(request, pk):
	template_name = "questions/detail.html"
	question = get_object_or_404(Question, pk=pk)

	context = {'question': question}
	comments = question.questioncomment_set.all().order_by('comment_date')
	
	paginator = Paginator(comments, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(context, request, False)
	
	return render(request, template_name, context)

def last_questions(request, days):
	template_name = "questions/index.html"
	time = timezone.now() - datetime.timedelta(days=days)
	questions = Question.objects.filter(
		question_date__gte=time, question_date__lte=timezone.now()
	).order_by('-question_date')
	context = {}
	paginator = Paginator(questions, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	context['title'] = 'Questions from Last ' + str(days) + ' day(s)'
	set_context(context, request)
	
	return render(request, template_name, context)

def category_detail(request, pk):
	template_name = "questions/category_detail.html"
	category = get_object_or_404(Category, pk=pk)
	context = {
		'category': category
	}
	set_context(context, request)
	questions = category.question_set.all().order_by('-question_date')
	
	paginator = Paginator(questions, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	
	return render(request, template_name, context)

def comment(request, pk):
	"""
	Comment on a given Question
	"""
	if request.method == 'POST':
		question = get_object_or_404(Question, pk=pk)
		
		# check if there are some comments with the same details
		# email and textmust be unique for every comment
		comments = QuestionComment.objects.filter(
			comment_text=request.POST['comment_text'],
			by_email=request.POST['by_email'])
		if comments: # comments are found, redirect
			return HttpResponseRedirect(reverse('questions:detail', args=(question.id,)))

		comment = QuestionComment(
			comment_for = question,
			comment_by = request.POST['comment_by'],
			by_email = request.POST['by_email'],
			comment_text = request.POST['comment_text'],
			comment_date = timezone.now(),
		)
		comment.save()
		return HttpResponseRedirect(reverse('questions:detail', args=(question.id,)))
	else:
		return HttpResponseRedirect(reverse('questions:index'))