from django.urls import path

from .views import PostList, PostDetail, PostCreate, PostDelete, PostEdit, PostSearch

urlpatterns = [
    path('', PostList.as_view(), name='post_list'),
    path('', PostList.as_view(), name='news'),
    path('<int:pk>/', PostDetail.as_view(), name='post_detail'),
    path('create/', PostCreate.as_view(), name='post_create'),
    path('<int:pk>/edit/', PostEdit.as_view()),
    path('news/create/', PostCreate.as_view(), name='post_create'),
    path('news/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('news/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),
    path('post_create/', PostCreate.as_view(), name='post_create'),
    path('search/', PostSearch.as_view()),
    path('articles/create/', PostCreate.as_view(), name='post_create'),
    path('articles/<int:pk>/edit', PostEdit.as_view(), name='post_edit'),
    path('articles/<int:pk>/delete', PostDelete.as_view(), name='post_delete'),

]
