# Generated by Django 3.0.5 on 2020-04-28 19:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0012_question_answer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='answer',
            name='content',
        ),
    ]