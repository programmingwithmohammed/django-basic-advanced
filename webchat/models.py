# Create your models here.
from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
from markdown import markdown
from django.utils.html import mark_safe

class ChatBoard(models.Model):
    name = models.CharField(max_length = 35, unique = True)
    details = models.CharField(max_length = 150)

    def __str__(self):
        return self.name

    #to get the number of post
    def get_posts_count(self):
        return Post.objects.filter(topic__boardName=self).count()

    #to get the last post
    def get_last_post(self):
        return Post.objects.filter(topic__boardName=self).order_by('createdBy').first()

class ChatTopic(models.Model):
    subject = models.CharField(max_length = 250)
    lastUpdate = models.DateTimeField(auto_now_add = True)
    boardName = models.ForeignKey(ChatBoard, related_name='topics',on_delete=models.CASCADE)
    boardStarter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)
    views = models.PositiveIntegerField(default=0)

    def __str__(self):
        return self.subject

class Post(models.Model):
    message = models.TextField(max_length = 5000)
    topic = models.ForeignKey(ChatTopic, related_name = 'posts',on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(null = True)
    createdBy = models.ForeignKey(User, related_name = 'posts',on_delete=models.CASCADE)
    updatedBy = models.ForeignKey(User, null = True, related_name = '+',on_delete=models.CASCADE)

    def __str__(self):
        truncated_message = Truncator(self.message)
        return truncated_message.chars(35)

    def get_message_as_markdown(self):
        return mark_safe(markdown(self.message, sefe_mode='escape'))
