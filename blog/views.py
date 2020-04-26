from django.views import generic
from .models import Post
from .forms import CommentForm
from django.shortcuts import render, get_object_or_404, HttpResponseRedirect
from django.core.paginator import (Paginator, PageNotAnInteger, EmptyPage)
from django.urls import reverse

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

	template_name = 'index.html'
	
	return render(
		request, template_name,
		{
			'Page': page,
			'post_list': post_list
		}
	)

def post_detail(request, slug):
	template_name = 'post_detail.html'
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

			return HttpResponseRedirect(reverse('post_detail', args=(post.slug, )))
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