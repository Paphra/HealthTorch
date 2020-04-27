from django.contrib.syndication.views import Feed
from django.template.defaultfilters import truncatewords
from django.urls import reverse

from .models_posts import Post

class LatestPostsFeed(Feed):
	title = 'Health Torch'
	link =""
	description = "Latest Posts on HealthTorch Uganda."

	def items(self):
		return Post.objects.filter(status=1)
	
	def item_title(self, item):
		return item.title
	
	def item_description(self, item):
		return truncatewords(item.content, 30)