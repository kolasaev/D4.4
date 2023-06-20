from django.shortcuts import render
from django.views.generic import View, ListView, DetailView,UpdateView,CreateView,TemplateView
from .models import Post, PostCategory,Malling,CategorySubscriber,Category
from datetime import datetime
from django.core.paginator import Paginator
from .filters import PostFilter
from .forms import PostForm
from django.http import HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect
from django.contrib.auth.models import Group
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string



class NewsList(ListView):
    model = Post
    template_name = 'news.html'
    context_object_name = 'news'
    ordering = ['-id']
    paginate_by = 3


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
        return context



class ArticleList(DetailView):

    queryset = Post.objects.all()
    template_name = 'article.html'
    context_object_name = 'news'


class MyView(PermissionRequiredMixin, View):
    permission_required = ('<app>.<action>_<model>',
                           '<app>.<action>_<model>')


class AddList(CreateView):
    queryset = Post.objects.all()
    template_name = 'add.html'
    #permission_required = ('news.add_post',)
    form_class = PostForm


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filter'] = PostFilter(self.request.GET, queryset=self.get_queryset())
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

class PostCategory(ListView):
    model = Post
    template_name = 'news.html'
    #context_object_name = 'news'
    ordering = ['-id']

    def get_queryset(self):
        self.id = resolve(self,requests.path_info).kwargs['pk']
        c = Category.objects.get(id=self.id)
        queryset=Post.objects.filter(categories=c)


class CategorySubscribers(LoginRequiredMixin, TemplateView):
    template_name = 'subscribed.html'
    model = CategorySubscriber


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        CategorySubscriber.objects.create(user=self.request.user, categoryType=Category.objects.get(pk=context['pk']))
        context['subscribed'] = Category.objects.get(pk=context['pk'])
        return context


class CategoryUnSubscribers(LoginRequiredMixin, TemplateView):
    template_name = 'unsubscribed.html'
    model = CategorySubscriber

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        delete_subcription = CategorySubscribers.objects.get(user=self.request.user,category=Category.objects.get(pk=context['pk']))
        delete_subcription.delete()
        context['unsubscribed'] = Category.objects.get(pk=context['pk'])
        return context



class MallingView(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'malling.html', {})

    def post(self, request, *args, **kwargs):
        malling = Malling(
            date=datetime.strptime(request.POST['date'], '%Y-%m-%d'),
            client_name=request.POST['user_name'],
            message=request.POST['message'],
        )
        appointment.save()

        # получем наш html
        html_content = render_to_string(
            'malling_created.html',
            {
                'malling': malling,
            }
        )

        # в конструкторе уже знакомые нам параметры, да? Называются правда немного по другому, но суть та же.
        msg = EmailMultiAlternatives(
            subject=f'{malling.user_name} {malling.date.strftime("%Y-%M-%d")}',
            body=appointment.message,  # это то же, что и message
            from_email='KolasMamaev@ya.ru',
            to=['kolasmamaev@gmail.com'],  # это то же, что и recipients_list
        )
        msg.attach_alternative(html_content, "text/html")  # добавляем html

        msg.send()  # отсылаем

        return redirect('malling:malling')