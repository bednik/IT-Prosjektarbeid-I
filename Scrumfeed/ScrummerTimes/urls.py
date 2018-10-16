from django.conf.urls import url
from . import views

urlpatterns = [
    #path that is nothing r'^$'
  url(r'^$', views.feed, name='feed'),
  url('feed/', views.feed, name='feed'),
  url('createArticle/', views.createarticle, name='createarticle'),
  url('myarticles/', views.myarticles, name='myarticles'),
  url('managesite/', views.manage_site, name='managesite'),
  url('analytics/', views.analytics, name='analytics'),
  #(?P) = paramaters <id> = parameter, \d+ d = digit, + = one or more digits, \$ = end
  url(r'^article/(?P<id>\d+)/$', views.article, name='article'),
  url(r'^article/edit/(?P<id>\d+)/$', views.editarticle, name='editarticle'),
  url(r'^feedUnread$', views.proofreading_feed, name='Proofreading')
]