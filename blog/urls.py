from django.urls import path

from . import views
from .views import index

urlpatterns = [
    path('', views.index, name='index'),
   # path('articles/', views.index2, name='articles'),

    path('articles/', views.ArticleListView.as_view(), name='articles'),
 #   path('', views.new_person, name='person-create'),

]