# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class ChatBoard(models.Model):
    name = models.CharField(max_length = 35, unique = True)
    details = models.CharField(max_length = 150)

    def __str__(self):
        return self.name

class ChatTopic(models.Model):
    subject = models.CharField(max_length = 250)
    lastUpdate = models.DateTimeField(auto_now_add = True)
    boardName = models.ForeignKey(ChatBoard, related_name='topics',on_delete=models.CASCADE)
    boardStarter = models.ForeignKey(User, related_name='topics',on_delete=models.CASCADE)

class Post(models.Model):
    message = models.TextField(max_length = 5000)
    topic = models.ForeignKey(ChatTopic, related_name = 'posts',on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add = True)
    updatedAt = models.DateTimeField(null = True)
    createdBy = models.ForeignKey(User, related_name = 'posts',on_delete=models.CASCADE)
    updatedBy = models.ForeignKey(User, null = True, related_name = '+',on_delete=models.CASCADE)
