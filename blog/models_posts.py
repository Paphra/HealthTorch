from django.db import models
from django.contrib.auth.models import User
from .models import Category, Image


STATUS = (
	(0, "Draft"),
	(1, 'Publish')
)


class Post(models.Model):
	title = models.CharField(max_length=200, unique=True)
	slug = models.SlugField(max_length=200, unique=True)
	author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_posts')
	updated_on = models.DateTimeField(auto_now=True)
	content = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS, default=0)
	category = models.ForeignKey(
		Category, on_delete=models.SET_NULL, null=True, blank=True,
		related_name='posts')
	image = models.ForeignKey(
		Image, on_delete=models.SET_NULL, null=True, blank=True)
	
	class Meta:
		ordering = ['-created_on']
	
	def __str__(self):
		return self.title
	
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("blog:posts_detail", kwargs={"slug": str(self.slug)})
	
class PostComment(models.Model):
	"""
	Coments for Posts
	"""
	name = models.CharField( max_length=100)
	email = models.EmailField(max_length=100)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	post = models.ForeignKey(
		Post, on_delete=models.CASCADE, related_name="comments")
	active = models.BooleanField(default=False)


	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return 'Comment on {} by {}'.format(self.post, self.name)