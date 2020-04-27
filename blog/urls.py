from . import views, views_posts, views_questions
from django.urls import path
from .feeds import LatestPostsFeed

app_name = 'blog'
urlpatterns = [
		#path('', views.post_list, name='home'),		
    path("feed/rss", LatestPostsFeed(), name='post_feed'),
		path('<slug:slug>/', views.post_detail, name='post_detail'),
		
		# index
		path('', views.index, name="index" ),
		path('categories', views.categories, name="categories"),
		path('about', views.about, name='about'),
		path('filter', views.filter, name="filter"),
		path('search', views.search, name="search"),
		path('subscribe', views.subscribe, name="subscribe"),
		path('subscribed/<int:pk>/', views.subscribed, name="subscribed"),
		path('unsubscribe/<int:pk>/', views.unsubscribe, name="unsubscribe"),
		path('unsubscribed/<int:pk>/', views.unsubscribed, name="unsubscribed"),
		path('resubscribe/<int:pk>/', views.resubscribe, name="resubscribe"),
		
		path('admin/images/', views.images, name="images"),
		path('admin/images/group/<int:pk>/', views.images_group, name="images_group"),
		path('admin/images/<int:image_id>/', views.image_detail, name="image_detail"),

		# posts
		path("posts", views_posts.index, name="posts_index"),
		path('posts/<slug:slug>/', views_posts.detail, name='posts_detail'),
		path('posts/last/<int:days>/', views_posts.last_posts, name='posts_last'),
		path('posts/categories/<int:pk>/', views_posts.category_detail, name='posts_category'),

		# questions
		path("questions", views_questions.index, name="questions_index"),
		path("questions/ask", views_questions.ask, name='questions_ask'),
		path('questions/<int:pk>/', views_questions.detail, name='questions_detail'),
		path('questions/last/<int:days>/', views_questions.last_questions, name='questions_last'),
		path('questions/categories/<int:pk>/', views_questions.category_detail, name='questions_category'),

		path('logout', views.logout, name="logout")
]
