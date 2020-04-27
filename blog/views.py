import base64
import datetime
from django.views import generic
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
from django.contrib.postgres.search import SearchQuery, SearchVector

from .models import Image, ImageGroup, Category, Subscriber, About
from .models_posts import Post
from .models_questions import Question


def set_context(context, request, search=True):
	context['c_user'] = request.user
	context['search'] = search
	context['categories'] = Category.objects.all()

def post_list(request):
	object_list = Post.objects.filter(status=1).order_by('-created_on')
	
	paginator = Paginator(object_list, 3)
	page = request.GET.get('page')
	try:
		post_list = paginator.page(page)
	except PageNotAnInteger:
		post_list = paginator.page(1)
	except EmptyPage:
		post_list = paginator.page(paginator.num_pages)

	template_name = 'blog/index.html'
	
	return render(
		request, template_name,
		{
			'Page': page,
			'post_list': post_list
		}
	)

def post_detail(request, slug):
	template_name = 'posts/post_detail.html'
	post = get_object_or_404(Post, slug=slug)
	comments = post.comments.filter(active=True)
	new_comment = None

	# Comment Posted
	if request.method == 'POST':
		comment_form = CommentForm(data=request.POST)
		if comment_form.is_valid():
			# Create Comment Object but don't dave to database yet
			new_comment = comment_form.save(commit=False)
			# Assign the current post to the comment
			new_comment.post = post
			#save the comment to the database
			new_comment.save()

			return HttpResponseRedirect(reverse('blog:posts_detail', args=(post.slug, )))
	else:
		comment_form = CommentForm()
	
	return render(
		request, template_name,
		{
			'post': post,
			'comments': comments,
			'new_comment': new_comment,
			'comment_form': comment_form
		}
	)

def about(request):
	author_group = Group.objects.filter(name="Author")[0]
	authors = User.objects.filter(groups=author_group.id)
	about = About.objects.all()
	
	if about:
		about = about[0]

	return render(	
		request,
		"blog/about.html",
		{
			'authors': authors,
			'about': about,
			'atabout': True,
			"c_user": request.user,
			"title": "About Us"
		}
	)

def convert_image(file):
	blob = file.read()
	b64 = base64.b64encode(blob)
	img_str = b64.decode('UTF-8')
	return img_str	

def index(request):
	"""
	returns the: 
	1. recent three posts
	2. recent three questions
	3. the partners list
	4. the doctors list
	"""
	latest_posts = Post.objects.filter(status=1).order_by('-created_on')[:3]
	other_posts = Post.objects.filter(status=1).order_by('-created_on')[3:15]
	categories = Category.objects.all()
	return render(
		request,
		"blog/index.html",
		{
			'title': 'Home',
			'search': True,
			'latest_posts': latest_posts,
			'other_posts': other_posts,
			'categories': categories,
			'athome': True,
			'c_user': request.user
		}
	)	


def categories(request):
	template_name = "blog/categories.html"
	categories = Category.objects.all()
	context = {
		'categories': categories,
		'c_user': request.user,
		'title': 'Categories',
		'atcategories': True,
	}
	
	return render(request, template_name, context)

# START Filter VIEW
def filter(request):
	template = "blog/filter.html"
	context = {
		'c_user': request.user,
		'search': True,
		'categories': Category.objects.all()
	}
	section = request.GET.get('section')
	month = request.GET.get('month')
	year = int(request.GET.get('year'))
	items = []
	if month == 'all':
		if section == 'Posts':
			context['atposts'] = True
			context['title'] = 'Filtered Posts for ' + str(year) + '/' +str(month)
			items = Post.objects.filter(
				created_on__year=year).order_by('-created_on')
		else:
			context['atquestions'] = True
			context['title'] = 'Filtered Questions for ' + str(year) + '/' +str(month)
			items = Question.objects.filter(
				question_date__year=year).order_by('-question_date')
	else:
		month = int(month)
		if section == 'Posts':
			context['atposts'] = True
			context['title'] = 'Filtered Posts for ' + str(year) + '/' +str(month)
			items = Post.objects.filter(
				created_on__year=year, 
				created_on__month=month).order_by('-created_on')
		else:
			context['atquestions'] = True
			context['title'] = 'Filtered Questions for ' + str(year) + '/' +str(month)
			items = Question.objects.filter(
				question_date__year=year,
				question_date__month=month).order_by('-question_date')
	
	context['f_year'] = year
	context['f_month'] = month
	paginator = Paginator(items, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	return render(request, template, context)
# END Filter VIEW

# START Images VIEWS
def SaveImage(request):
	file = request.FILES['image']
	img_str = convert_image(file)
	image = Image(
		title = request.POST['title'],
		data = img_str,
		group = ImageGroup.objects.get(pk=request.POST['group']),
			description = request.POST['description'],
	)
	image.save()
	return HttpResponseRedirect(reverse("blog:image_detail", args=(image.id,)))

def images(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/admin')
	if request.method == "POST":
		return SaveImage(request)
	else:
		groups = ImageGroup.objects.all()
		return render(
			request,
			'blog/images.html',
			{
				"title": "Images",
				"c_user": request.user,
				"groups": groups,
				'atimages': True,
			}
		)

def images_group(request, pk):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/admin')
	if request.method == "POST":
		return SaveImage(request)
	
	else:
		template_name = 'blog/images_group.html'
		group = get_object_or_404(ImageGroup, pk=pk)
		images = group.images.all()
		context = {
			'title': "Images in " + group.name,
			'group': group,
			'groups': ImageGroup.objects.all(),
		}

		paginator = Paginator(images, 30) # Show 20 per page.
		page_number = request.GET.get('page')
		page_obj = paginator.get_page(page_number)
		context['page_obj'] = page_obj
		set_context(context, request, False)
		return render(request, template_name, context)

def image_detail(request, image_id):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/admin')
	old_image = get_object_or_404(Image, pk=image_id)
	groups = ImageGroup.objects.all()
	if request.method == "POST":
		old_image.title = request.POST['title']
		old_image.group = groups.get(pk=request.POST['group'])
		old_image.description = request.POST['description']
		if request.FILES:
			old_image.data = convert_image(request.FILES['image'])
		old_image.save()

		return HttpResponseRedirect(reverse('blog:image_detail', args=(old_image.id,)))
	else:
		return render(
			request,
			"blog/image_detail.html",
			{
				'title': 'Image',
				'image': old_image,
				'groups': groups,
				'c_user': request.user,
				'atimages': True,
			} 
		)
#END Images VIEWS

# START Search VIEW
@csrf_exempt
def search(request):
	section = request.GET.get('s')
	phrase = request.GET.get('q')
	query = SearchQuery(phrase)
	items = []

	context = {
		'title': 'Search Results',
		'query': phrase,
		'section': section,
		'search': True,
		'categories': Category.objects.all(),
		'c_user': request.user,
	}

	if section == 'Posts':
		context['atposts'] = True
		post_vector = SearchVector('title') + SearchVector('content')
		items = Post.objects.annotate(
			search=post_vector).filter(search=query).order_by('-created_on')
	else:
		context['atquestions'] = True
		question_vector = SearchVector('question_text')
		items = Question.objects.annotate(
			search=question_vector).filter(search=query).order_by('-question_date')
	
	paginator = Paginator(items, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	
	return render(request, 'blog/search.html', context)
	
#END Search VIEW

# START Subscribe VIEWS
def subscribe(request):
	if request.method == "POST":
		# Check for the subscriber to see if already exists
		subscribers = Subscriber.objects.filter(email=request.POST['email'])
		if subscribers: # some subscribers with the email are found
			subscribers[0].subscribed = True # subscribe the first one
			subscribers[0].save()	# save him/her then redirect
			return HttpResponseRedirect(reverse('blog:subscribed', args=(subscribers[0].id,)))
		subscriber = Subscriber(
			first_name = request.POST['first_name'],
			last_name = request.POST['last_name'],
			email = request.POST['email'],
			subscribed = True,
		)

		subscriber.save()
		return HttpResponseRedirect(reverse('blog:subscribed', args=(subscriber.id,)))
	else:
		return HttpResponseRedirect(reverse('blog:index'))

def subscribed(request, pk):
	subscriber = get_object_or_404(Subscriber, pk=pk)
	return render(request, 'blog/subscribed.html', {
		'title': 'Successfully Subscribed',
		'c_user': request.user,
		'subscriber': subscriber,
		'subscribed': True,
	})

@csrf_exempt
def unsubscribe(request, pk):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('blog:index'))
	subscriber = get_object_or_404(Subscriber, pk=pk)
	c_subscriber = get_object_or_404(Subscriber, pk=int(request.POST['subscriber']))
	c_subscriber.subscribed = False
	c_subscriber.save()
	return HttpResponseRedirect(reverse('blog:unsubscribed', args=(subscriber.id,)))

def unsubscribed(request, pk):
	subscriber = get_object_or_404(Subscriber, pk=pk)
	return render(request, 'blog/subscribed.html', {
		'title': 'Successfully Unsubscribed',
		'c_user': request.user,
		'subscriber': subscriber,
		'subscribed': False,
	})

def resubscribe(request, pk):
	if request.method != 'POST':
		return HttpResponseRedirect(reverse('blog:index'))
	subscriber = get_object_or_404(Subscriber, pk=pk)
	c_subscriber = get_object_or_404(Subscriber, pk=int(request.POST['subscriber']))
	c_subscriber.subscribed = True
	c_subscriber.save()
	return HttpResponseRedirect(reverse('blog:subscribed', args=(subscriber.id,)))

# END Subscribe VIEWS


def logout(request):
	return HttpResponseRedirect('/admin/logout')