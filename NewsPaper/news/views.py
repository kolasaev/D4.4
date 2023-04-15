from django.shortcuts import render
from django.views.generic import ListView, DetailView,UpdateView,CreateView
from .models import Post, PostCategory
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponse



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
    context_object_name = 'news'
    context_object_name = 'news'


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





class EditList(UpdateView):
    #queryset = Post.objects.all()
    template_name = 'edit.html'
    #context_object_name = 'news'
    form_class = PostForm

    def get_object(self, **kwargs):
        id = self.kwargs.get('pk')
        return Post.objects.get(pk=id)




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
