from django.db import models
from django.contrib.auth.models import User
from .models import Category

from django_summernote.fields import SummernoteTextField

STATUS = (
	(0, "Draft"),
	(1, 'Publish')
)

ANSWER = (
	(0, 'Not Answered'),
	(1, 'Answered')
)
	
class Question(models.Model):
	name = models.CharField('Full Name', max_length=100)
	email = models.EmailField("Email Address", max_length=100)
	updated_on = models.DateTimeField(auto_now=True)
	content = models.TextField(verbose_name='Question')
	created_on = models.DateTimeField(auto_now_add=True)
	status = models.IntegerField(choices=STATUS, default=0)
	category = models.ForeignKey(
		Category, on_delete=models.SET_NULL, null=True, blank=True,
		related_name='questions')
	answer = models.IntegerField(choices=ANSWER, default=0)

	class Meta:
		ordering = ['-created_on']
	
	def __str__(self):
		return self.name + ' | ' + self.email 
	
	def get_absolute_url(self):
		from django.urls import reverse
		return reverse("blog:questions_detail", kwargs={"pk": str(self.pk)})
		
class Answer(models.Model):
	user = models.ForeignKey(
		User, on_delete=models.CASCADE)
	content = SummernoteTextField()
	question = models.ForeignKey(
		Question, on_delete=models.CASCADE, related_name='answers')
	created_on = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		return "Answer to {}.".format(self.question)


class QuestionComment(models.Model):
	"""
	Coments for Questions
	"""
	name = models.CharField(max_length=50)
	email = models.EmailField(max_length=100)
	body = models.TextField()
	created_on = models.DateTimeField(auto_now_add=True)
	question = models.ForeignKey(
		Question, on_delete=models.CASCADE, related_name="comments")
	active = models.BooleanField(default=False)


	class Meta:
		ordering = ['-created_on']

	def __str__(self):
		return 'Comment on {} by {}'.format(self.question, self.name)