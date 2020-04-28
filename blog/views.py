import base64
import datetime
from django.views import generic
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)
from django.contrib.auth.models import Group, User

from django.views.decorators.csrf import csrf_exempt
from django.urls import reverse
from django.utils import timezone
from django.contrib.postgres.search import SearchQuery, SearchVector

from .models import Image, ImageGroup, Category, Subscriber, About, Partner
from .models_posts import Post
from .models_questions import Question


def set_context(request, context, search=True):
	context['c_user'] = request.user
	context['search'] = search
	context['categories'] = Category.objects.all()
	context['partners'] = Partner.objects.filter(active=True)
	
def about(request):
	author_group = Group.objects.filter(name="Authors")[0]
	authors = User.objects.filter(groups=author_group.id)
	about = About.objects.all()
	
	if about:
		about = about[0]

	context = {
			'authors': authors,
			'about': about,
			'atabout': True,
			"title": "About Us"
		}
	set_context(request, context, False)

	return render(	
		request,
		"blog/about.html",
		context
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
	context = {
			'title': 'Home',
			'latest_posts': latest_posts,
			'other_posts': other_posts,
			'athome': True,
		}
	set_context(request, context)
	return render(
		request,
		"blog/index.html",
		context
	)	


def categories(request):
	template_name = "blog/categories.html"
	context = {
		'title': 'Categories',
		'atcategories': True,
	}
	set_context(request, context)

	return render(request, template_name, context)

# START Filter VIEW
def filter(request):
	template = "blog/filter.html"
	context = {}
	section = request.GET.get('section')
	month = request.GET.get('month')
	year = int(request.GET.get('year'))
	items = []
	if month == 'all':
		if section == 'Posts':
			context['atposts'] = True
			context['title'] = 'Filtered Posts for ' + str(year) + '/' +str(month)
			items = Post.objects.filter(
				created_on__year=year, status=1).order_by('-created_on')
		else:
			context['atquestions'] = True
			context['title'] = 'Filtered Questions for ' + str(year) + '/' +str(month)
			items = Question.objects.filter(
				created_on__year=year, status=1).order_by('-created_on')
	else:
		month = int(month)
		if section == 'Posts':
			context['atposts'] = True
			context['title'] = 'Filtered Posts for ' + str(year) + '/' +str(month)
			items = Post.objects.filter(
				created_on__year=year, 
				created_on__month=month, status=1).order_by('-created_on')
		else:
			context['atquestions'] = True
			context['title'] = 'Filtered Questions for ' + str(year) + '/' +str(month)
			items = Question.objects.filter(
				created_on__year=year,
				created_on__month=month, status=1).order_by('-created_on')
	
	context['f_year'] = year
	context['f_month'] = month
	paginator = Paginator(items, 20) # Show 20 per page.
	page_number = request.GET.get('page')
	page_obj = paginator.get_page(page_number)
	context['page_obj'] = page_obj
	set_context(request, context)

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
		context = {
				"title": "Images",
				"groups": groups,
				'atimages': True,
			}
		set_context(request, context, False)
		return render(
			request,
			'images/index.html',
			context
		)

def images_group(request, pk):
	if not request.user.is_authenticated:
		return HttpResponseRedirect('/admin')
	if request.method == "POST":
		return SaveImage(request)
	else:
		template_name = 'images/images_group.html'
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
	
	context = {
		'title': 'Image',
		'image': old_image,
		'groups': groups,
		'atimages': True,
	} 
	set_context(request, context, False)

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
			"images/image_detail.html",
			context
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
		'section': section
	}
	set_context(request, context, True)

	if section == 'Posts':
		context['atposts'] = True
		post_vector = SearchVector('title') + SearchVector('content')
		items = Post.objects.annotate(
			search=post_vector).filter(search=query, status=1).order_by('-created_on')
	else:
		context['atquestions'] = True
		question_vector = SearchVector('content')
		items = Question.objects.annotate(
			search=question_vector).filter(search=query, status=1).order_by('-created_on')
	
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
	context = {
		'title': 'Successfully Subscribed',
		'subscriber': subscriber,
		'subscribed': True,
	}
	set_context(request, context, False)

	return render(request, 'blog/subscribed.html', context)

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
	context = {
		'title': 'Successfully Unsubscribed',
		'subscriber': subscriber,
		'subscribed': False,
	}
	set_context(request, context, False)
	return render(request, 'blog/subscribed.html', context)

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