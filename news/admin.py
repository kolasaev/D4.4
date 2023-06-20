from django.contrib import admin
from .models import Post, PostCategory
import datetime

admin.site.register(Post)
admin.site.register(PostCategory)
