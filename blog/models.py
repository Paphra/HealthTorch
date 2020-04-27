from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver

class Category(models.Model):
	"""
	The Categories of the posts under which they are made
	"""
	name = models.CharField(max_length=30)

	def __str__(self):
			return self.name

class ImageGroup(models.Model):
	"""
	Stores the image groups forexample:
		1. Users
		2. Posts
		3. Questions etc
	"""
	name = models.CharField(max_length=50)
	description = models.TextField(blank=True)

	def __str__(self):
		return self.name

class Image(models.Model):
	""" 
	Stores all the images of the System
	"""
	title = models.CharField(max_length=50)
	data = models.TextField(blank=True)
	group = models.ForeignKey(
		ImageGroup, on_delete=models.SET_NULL, null=True, blank=True,
		related_name="images")
	description = models.TextField(blank=True)
	
	def __str__(self):
		return self.title

class Profile(models.Model):
	"""
	Stores extra information about the user
	"""
	user = models.OneToOneField(
		User, on_delete=models.CASCADE)
	title = models.CharField(max_length=30, blank=True)
	bio = models.TextField(blank=True)
	address = models.CharField(max_length=100, blank=True)
	qualification = models.CharField(max_length=100, blank=True)
	profession = models.CharField(max_length=100, blank=True)
	employment = models.CharField(max_length=100, blank=True)
	position = models.CharField(max_length=100, blank=True)
	experience = models.PositiveIntegerField(default=0)
	image = models.ForeignKey(
		Image, on_delete=models.SET_NULL, null=True, blank=True)

	def __str__(self):
		return self.title +' ' + self.user.first_name + ' ' + self.user.last_name 
	
@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
	if created:
		Profile.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()

class Subscriber(models.Model):
	"""
	Store all the Users Who Subscribe for timely updates
	"""
	first_name = models.CharField(max_length=30)
	last_name = models.CharField(max_length=30)
	email = models.EmailField(max_length=100)
	subscribed = models.BooleanField(default=True)

	def __str__(self):
		return self.email
	
	def name(self):
		return self.first_name + ' ' + self.last_name

class About(models.Model):
	site_title = models.CharField(max_length=200)
	info = models.TextField('About Us')
	last_modified = models.DateTimeField('date modified')

	def __str__(self):
		return "About Us"