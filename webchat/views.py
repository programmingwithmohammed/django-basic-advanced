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
from django.db.models import Count
from django.utils import timezone
from django.views.generic import UpdateView
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger
from django.views.generic import ListView
from django.urls import reverse_lazy
from django.urls import reverse


#function based view home- FBC
def home(request):
    chatBoard = ChatBoard.objects.all()
    return render(request, 'home.html',{'chatBoard':chatBoard})

#class based view -home
# class BoardListView(ListView):
#     model = ChatBoard
#     context_object_name = 'boards'
#     template_name = 'home.html'

#FBV -board_topic
# def board_topic(request,pk):
#     #chat_board = ChatBoard.objects.get(pk=pk)
#     chat_board = get_object_or_404(ChatBoard, pk=pk)

#     queryset = chat_board.topics.order_by('-lastUpdate').annotate(replies=Count('posts') -1)
#     page = request.GET.get('page',1)

#     paginator = Paginator(queryset, 20)

#     try:
#         topics = paginator.page(page)
#     except PageNotAnInteger:
#         topics = paginator.page(1)
#     except EmptyPage:
#         topics = paginator.page(paginator.num_pages)

#     #topics = chat_board.topics.order_by('-lastUpdate').annotate(replies=Count('posts')-1)
#     return render(request, 'chat_board_topics.html', {'chat_board': chat_board, 'topics':topics})

#CBV -board_topic
class TopicListView(ListView):
    model = ChatTopic
    context_object_name = 'topics'
    template_name = 'chat_board_topics.html'
    paginate_by = 10

    def get_context_data(self, **kwargs):
        kwargs['chat_board'] = self.chat_board
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.chat_board = get_object_or_404(ChatBoard, pk = self.kwargs.get('pk'))
        queryset = self.chat_board.topics.order_by('-lastUpdate').annotate(replies=Count('posts') - 1)
        return queryset


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


#FBV-topic_posts
# def topic_posts(request, pk, topic_pk):
#     topic = get_object_or_404(ChatTopic, boardName__pk=pk, pk=topic_pk )
#     topic.views += 1
#     topic.save()
#     return render(request, 'topic_posts.html', {'topic':topic})

#CBV -topic_posts
class PostListView(ListView):
    model = Post
    context_object_name = 'posts'
    template_name = 'topic_posts.html'
    paginate_by = 3

    def get_context_data(self, **kwargs):

        session_key = 'viewd_topic_{}'.format(self.topic.pk)
        if not self.request.session.get(session_key, False):
            self.topic.views += 1
            self.topic.save()
            self.request.session[session_key] = True

        kwargs['topic'] = self.topic
        return super().get_context_data(**kwargs)

    def get_queryset(self):
        self.topic = get_object_or_404(ChatTopic,boardName__pk=self.kwargs.get('pk'), pk=self.kwargs.get('topic_pk'))
        queryset = self.topic.posts.order_by('createdAt')
        return queryset

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

            topic.lastUpdate = timezone.now()
            topic.save()

            topic_url = reverse('topic_posts', kwargs={'pk':pk, 'topic_pk':topic_pk})
            topic_post_url = '{url}?page={page}#{id}'.format(
                url=topic_url,
                id=post.pk,
                page=topic.get_page_count()
                )

            return redirect(topic_post_url)
    else:
        form = PostForm()
    return render(request,'reply_topic.html', {'topic':topic, 'form':form})


#CBV
@method_decorator(login_required, name='dispatch')
class PostUpdateView(UpdateView):
    model = Post
    fields = ('message',)
    template_name = 'edit_post.html'
    pk_url_kwarg = 'post_pk'
    context_object_name = 'post'

    def form_valid(self, form):
        post = form.save(commit=False)
        post.updatedBy = self.request.user
        post.updatedAt = timezone.now()
        post.save()
        return redirect('topic_posts', pk=post.topic.boardName.pk, topic_pk=post.topic.pk)


