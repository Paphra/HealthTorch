import datetime

from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.views import generic
from django.utils import timezone
from django.urls import reverse
from django.core.paginator import Paginator

from .models_posts import Post, PostComment
from .models import Category
from .forms import PostCommentForm


def set_context(context, request, search=True):
	context['c_user'] = request.user
	context['atposts'] = True
	context['search'] = search
	context['categories'] = Category.objects.all()

def index(request):
	template_name = "posts/index.html"
	posts = Post.objects.filter(status=1).order_by('-created_on')
	context = {
		'posts': posts,
		'title': 'Posts'
	}
	
	paginator = Paginator(posts, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(context, request)
	return render(request, template_name, context)	

def detail(request, slug):
	template_name = "posts/detail.html"
	post = get_object_or_404(Post, slug=slug)

	context = {
		'post': post,
		'title': post.title,
	}
	comments = post.comments.filter(active=True).order_by('created_on')
	
	paginator = Paginator(comments, 15)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(context, request, False)
	new_comment = None

	if request.method == 'POST':
		
		comment_form = PostCommentForm(data = request.POST)

		# check if there are some comments with the same details
		# email and textmust be unique for every comment
		comments = PostComment.objects.filter(
			body=request.POST['body'],
			email=request.POST['email'])

		if comments: # comments are found, redirect
			return HttpResponseRedirect(reverse('blog:posts_detail', args=(post.slug,)))

		if comment_form.is_valid():
			new_comment = comment_form.save(commit=False)
			new_comment.post = post
			new_comment.save()
	else:
		comment_form = PostCommentForm()
		
	context['new_comment'] = new_comment
	context['form'] = comment_form

	return render(request, template_name, context)

def last_posts(request, days):
	template_name = "posts/index.html"
	time = timezone.now() - datetime.timedelta(days=days)
	posts = Post.objects.filter(
		created_on__gte=time, created_on__lte=timezone.now(),
		status=1
	).order_by('-created_on')
	context = {}
	paginator = Paginator(posts, 20)
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	context['title'] = 'Posts from Last ' + str(days) + ' day(s)'
	set_context(context, request)
	
	return render(request, template_name, context)

def category_detail(request, pk):
	template_name = "posts/category_detail.html"
	category = get_object_or_404(Category, pk=pk)
	context = {
		'category': category,
		'title': category.name,
	}
	set_context(context, request)
	posts = category.posts.order_by('-created_on')
	
	paginator = Paginator(posts, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	
	return render(request, template_name, context)