from django.shortcuts import render
from django.views.generic import ListView, DetailView,UpdateView,CreateView,TemplateView
from .models import Post, PostCategory
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required



class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 1


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context



class ArticleList(DetailView):

    template_name = 'article.html'
    context_object_name = 'article'
    #context_object_name = 'news'


class AddList(CreateView):
    queryset = Post.objects.all()
    template_name = 'add.html'
    form_class = PostForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())

        # context['categoryType'] = categoryType.objects.all()
        context['form'] = PostForm()
        return context





class EditList(LoginRequiredMixin,UpdateView,):
    template_name = 'add.html'
    form_class = PostForm


    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)


@login_required
def upgrade_me(request):
    user = request.user
    avthor_group = Group.objects.get(name='avthor')
    if not request.user.groups.filter(name='avthor').exists():
        avthor_group.user_set.add(user)
    return redirect('/')







class DeleteList(DetailView):
    context_object_name = 'news'
    template_name = 'delete.html'
    queryset = Post.objects.all()
    success_url = '/news.html/'



class SearchList(ListView):
    model = Post
    template_name = 'search.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 1
    form_class = PostForm

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET,queryset=self.get_queryset())  # вписываем наш фильтр в контекст
        context['form'] = PostForm()
        return context
