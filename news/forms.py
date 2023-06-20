from django.forms import ModelForm
from .models import Post
from allauth.account.forms import SignupForm
from django.contrib.auth.models import Group
from django import forms
from django.contrib.auth.models import User


# Создаём модельную форму
class PostForm(ModelForm):
    # в класс мета, как обычно, надо написать модель, по которой будет строиться форма и нужные нам поля. Мы уже делали что-то похожее с фильтрами.
    class Meta:
        model = Post
        fields = ['text', 'title','dateCreation', 'categoryType','avthor']


class BasicSignupForm(SignupForm):
    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user