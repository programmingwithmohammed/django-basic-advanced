# -*- coding: utf-8 -*-
from django import forms
from .models import ChatTopic
from .models import Post



class NewChatTopicForm(forms.ModelForm):
    message = forms.CharField(
        widget = forms.Textarea(
            attrs = {'rows': 7, 'placeholder':'What you are thinking'}
        ),
        max_length=5000,
        help_text = 'The max length of the text is 5000.'
    )

    class Meta:
        model = ChatTopic
        fields = ['subject', 'message']


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['message']

