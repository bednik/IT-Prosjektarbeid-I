from django.conf.urls import url
from . import views

urlpatterns = [
    #path that is nothing r'^$'
  url(r'^$', views.feed, name='feed'),
  url('feed/', views.feed, name='feed'),
  url('createArticle/', views.createarticle, name='createarticle'),
  #(?P) = paramaters <id> = parameter, \d+ d = digit, + = one or more digits, \$ = end
  url(r'^article/(?P<id>\d+)/$', views.article, name='article'),
  url(r'^article/(?P<id>\d+)/edit/$', views.editarticle, name='editarticle'),
]