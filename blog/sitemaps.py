from django.contrib.sitemaps import Sitemap
from .models_posts import Post

class PostSitemap(Sitemap):
	changefreq = "daily"
	priority = 0.9

	def items(self):
		return Post.objects.filter(status=1)
	
	def lastmod(self, obj):
		return obj.updated_on