# Create your views here.
from django.shortcuts import render
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.http import HttpResponse
from .models import ChatBoard
from .models import ChatTopic
from .models import Post
from django.contrib.auth.models import User
from .forms import NewChatTopicForm



def home(request):
    chatBoard = ChatBoard.objects.all()
    return render(request, 'home.html',{'chatBoard':chatBoard})

def board_topic(request,pk):
    chat_board = ChatBoard.objects.get(pk=pk)
    return render(request, 'chat_board_topics.html', {'chat_board': chat_board})


def new_board_topic(request, pk):
    chat_board = get_object_or_404(ChatBoard, pk=pk)

    user = User.objects.first()

    if request.method == 'POST':
        form = NewChatTopicForm(request.POST)
        if form.is_valid():
            chatTopic = form.save(commit=False)
            chatTopic.chat_board = chat_board
            chatTopic.boardStarter = user
            chatTopic.save()

            post = Post.objects.create(
                message=form.cleaned_data.get('message'),
                topic=chatTopic,
                createdBy=user)
            return redirect('board_topic', pk=chat_board.pk)
    else:
        form = NewChatTopicForm()

    return render(request, 'new_board_topic.html', {'chat_board':chat_board, 'form':form})

