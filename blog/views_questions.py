import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator

from .models_questions import Question, QuestionComment, Answer
from .forms import QuestionForm, QuestionCommentForm
from .models import Category, Partner

# Create your views here.

def set_context(request, context, search=True):
	context['c_user'] = request.user
	context['atquestions'] = True
	context['search'] = search
	context['partners'] = Partner.objects.filter(active=True)
	context['categories'] = Category.objects.all()

def index(request):
	template_name = "questions/index.html"
	questions = Question.objects.filter(status=1).order_by('-created_on')
	context = {
		'questions': questions,
		'title': 'Questions'
	}
	
	paginator = Paginator(questions, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(request, context)
	return render(request, template_name, context)	

def ask(request):
	"""
	Allows asking a question
	"""
	template = "questions/ask.html"
	context = {
		'title': 'Ask A Question'
	}
	set_context(request, context, False)
	new_question = None

	if request.method == 'POST':
		question_form = QuestionForm(request.POST)

		questions = Question.objects.filter(
			content =request.POST['content'],
			email=request.POST['email'])

		if questions: # comments are found, redirect
			return HttpResponseRedirect(reverse('blog:questions_index'))

		if question_form.is_valid():
			new_question = question_form.save()

	else:
		question_form = QuestionForm()

	context['form'] = question_form
	context['new_question'] = new_question

	return render(request, template, context)

def detail(request, pk):

	template_name = "questions/detail.html"
	question = get_object_or_404(Question, pk=pk)

	context = {
		'question': question,
		'title': "Question " + str(question.id) + " Details",
	}
	comments = question.comments.filter(active=True).order_by('created_on')
	
	paginator = Paginator(comments, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(request, context, False)
	new_comment = None

	if request.method == 'POST':
		
		comment_form = QuestionCommentForm(data = request.POST)

		# check if there are some comments with the same details
		# email and textmust be unique for every comment
		comments = QuestionComment.objects.filter(
			body=request.POST['body'],
			email=request.POST['email'])

		if comments: # comments are found, redirect
			return HttpResponseRedirect(reverse('blog:questions_detail', args=(question.id,)))

		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.question = question
			new_comment.save()
	else:
		comment_form = QuestionCommentForm()
		
	context['new_comment'] = new_comment
	context['form'] = comment_form

	return render(request, template_name, context)

	
def last_questions(request, days):
	template_name = "questions/index.html"
	time = timezone.now() - datetime.timedelta(days=days)
	questions = Question.objects.filter( status=1,
		created_on__gte=time, created_on__lte=timezone.now()
	).order_by('-created_on')
	context = {}
	paginator = Paginator(questions, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	context['title'] = 'Questions from Last ' + str(days) + ' day(s)'
	set_context(request, context)
	
	return render(request, template_name, context)

def category_detail(request, pk):
	template_name = "questions/category_detail.html"
	category = get_object_or_404(Category, pk=pk)
	context = {
		'category': category,
		'title': category.name
	}
	set_context(request, context)
	questions = category.questions.filter(status=1).order_by('-created_on')
	
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