from django.urls import path

from . import views
from .views import index

urlpatterns = [
  #  path('', views.index, name='index'),article_detail    by_user
  #  path('authors/', views.AuthoreListView.as_view(), name='author_list'),
    path('user/<str:username>', views.view_user, name='view-user'),
    path('author/<int:pk>', views.AuthorDetailView.as_view(), name='author-detail'),
    path('author/<int:pk>/update/', views.AuthorUpdate.as_view(), name='author-update'),
   # path('author/<int:pk>', views.article_detail, name='author-detail'),
    path('articles/', views.ArticleListView.as_view(), name='article_list'),
    path('articles_user/', views.article_list_by_user, name='user_article_list'),
    path('article/<int:pk>', views.article_detail, name='article-detail'),
  #  path('article/<int:pk>', views.ArticleDetailView.as_view(), name='article-detail'),
    #path('article/new/', views.ArticleCreate.as_view(), name='article_new'),
    path('article/new/', views.article_new, name='article_new'),
    path('article/<int:pk>/edit/', views.article_edit, name='article_edit'),
   # path('article/', views.index2, name='articles'),
    path('comment/new/<int:pk>', views.comment_new, name='comment_new'),
    path('index/', views.ArticleListView.as_view(), name='article_list'),

#    path('', views.home, name='home'),

 #   path('', views.new_person, name='person-create'),

]