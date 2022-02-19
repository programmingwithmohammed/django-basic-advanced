# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import ChatBoard
from .models import ChatTopic
from .models import Post
from django.contrib.auth.models import User
from .forms import NewChatTopicForm, PostForm
from django.contrib.auth.decorators import login_required



def home(request):
    chatBoard = ChatBoard.objects.all()
    return render(request, 'home.html',{'chatBoard':chatBoard})

def board_topic(request,pk):
    #chat_board = ChatBoard.objects.get(pk=pk)
    chat_board = get_object_or_404(ChatBoard, pk=pk)
    return render(request, 'chat_board_topics.html', {'chat_board': chat_board})

@login_required
def new_board_topic(request, pk):
    chat_board = get_object_or_404(ChatBoard, pk=pk)
    #user = User.objects.first()
    if request.method == 'POST':
        form = NewChatTopicForm(request.POST)
        if form.is_valid():
            topic = form.save(commit=False)
            topic.boardName = chat_board #it was before chat_board (wrong)
            topic.boardStarter = request.user
            topic.save()

            Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=topic,
                createdBy=request.user
                )
            return redirect('topic_posts', pk=pk,topic_pk=topic.pk)
    else:
        form = NewChatTopicForm()

    return render(request, 'new_board_topic.html', {'chat_board':chat_board, 'form':form})



def topic_posts(request, pk, topic_pk):
    topic = get_object_or_404(ChatTopic, boardName__pk=pk, pk=topic_pk )
    return render(request, 'topic_posts.html', {'topic':topic})

@login_required
def reply_topic(request, pk, topic_pk):
    topic = get_object_or_404(ChatTopic, boardName__pk=pk, pk=topic_pk )
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.topic = topic
            post.createdBy = request.user
            post.save()
            return redirect('topic_posts', pk=pk, topic_pk=topic_pk)
    else:
        form = PostForm()
    return render(request,'reply_topic.html', {'topic':topic, 'form':form})

