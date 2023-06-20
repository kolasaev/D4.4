from django_filters import FilterSet
from .models import Post

class PostFilter(FilterSet):

    class Meta:
        model = Post
        search_fields=['avthor__name']
        fields = {
            'title': ['icontains'],
            'text': ['icontains'],
            #'avthor'.queryset: ['icontains'],
            'dateCreation': ['lt'],
            #'PostCategory':['icontains'],


        }