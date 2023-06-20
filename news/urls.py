from django.urls import path
from .views import NewsList, ArticleList,SearchList,AddList,EditList,DeleteList,CategorySubscribers,CategoryUnSubscribers

urlpatterns = [
    path('', NewsList.as_view()),
    path('<int:pk>', ArticleList.as_view(), name='article'),
    path('search/', SearchList.as_view(), name='search'),
    path('add/', AddList.as_view(), name='add'),
    path('edit/<int:pk>', EditList.as_view(), name='edit'),
    path('delete/<int:pk>', DeleteList.as_view(), name='delete'),
    path('subscribed/<int:pk>', CategorySubscribers.as_view(), name = 'subscribed'),
    path('unsubscribed/<int:pk>', CategoryUnSubscribers.as_view(), name = 'unsubscribed'),

]