# Импортируем класс, который говорит нам о том,
# что в этом представлении мы будем выводить список объектов из БД
from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, DeleteView, CreateView, UpdateView

from .filters import PostFilter
from .forms import PostForm
from .models import Post
from django.http import HttpResponse


class PostList(ListView):
    # Указываем модель, объекты которой мы будем выводить
    model = Post
    ordering = '-time_in'
    template_name = 'posts.html'
    # Это имя списка, в котором будут лежать все объекты.
    # Его надо указать, чтобы обратиться к списку объектов в html-шаблоне.
    context_object_name = 'posts'
    paginate_by = 10  # вот так мы можем указать количество записей на странице

    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['time_in'] = datetime.utcnow()
        return context


class PostDetail(DetailView):
    # Модель всё та же, но мы хотим получать информацию по отдельной новости
    model = Post
    # Используем другой шаблон — post.html
    template_name = 'post.html'
    # Название объекта, в котором будет выбранный пользователем пост
    context_object_name = 'post'


class PostSearch(ListView):
    model = Post
    ordering = '-time_in'
    filterset_class = PostFilter
    template_name = 'search.html'
    context_object_name = 'search'
    paginate_by = 10


    def get_queryset(self):
        queryset = super().get_queryset()
        self.filterset = PostFilter(self.request.GET, queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


class PostDelete(DeleteView):
    model = Post
    template_name = 'delete.html'
    context_object_name = 'post_delete'
    success_url = reverse_lazy('posts_list')


class PostCreate(CreateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.add_post'
    model = Post
    template_name = 'create.html'
    context_object_name = 'post_create'
    form_class = PostForm

    def form_valid(self, form):
        self.object = form.save(commit=False)
        if 'news' in self.request.path:
            choice_field = 'NE'
        elif 'articles' in self.request.path:
            choice_field = 'AR'
        self.object.choice_field = choice_field
        return super().form_valid(form)


class PostEdit(UpdateView, LoginRequiredMixin, PermissionRequiredMixin):
    permission_required = 'news.change_post'
    form_class = PostForm
    model = Post
    template_name = 'edit.html'
    context_object_name = 'post_edit'

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)



def index(request):
    return HttpResponse("Привет. Вы на главной странице приложения NewsPaper!")
