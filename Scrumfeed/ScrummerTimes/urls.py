from django.conf.urls import url
from . import views

urlpatterns = [
    #path that is nothing r'^$'
  url(r'^$', views.feed, name='feed'),
  url('feed/', views.feed, name='feed'),
  url('createArticle/', views.createarticle, name='createarticle'),
  url('requestRole/', views.requestrole, name='requestrole'),
  url(r'^assignRoles/(?P<id>\d+)/$', views.assignroles, name='assignroles'),
  url('myarticles/', views.myarticles, name='myarticles'),
  url('managesite/', views.manage_site, name='managesite'),
  url('stylesite/', views.styleChange, name='stylesite'),
  url('analytics/', views.analytics, name='analytics'),

  # (?P) = paramaters <id> = parameter, \d+ d = digit, + = one or more digits, \$ = end
  url(r'^article/(?P<id>\d+)/$', views.article, name='article'),
  url(r'^article/edit/(?P<id>\d+)/$', views.editarticle, name='editarticle'),
  url(r'^feedUnread$', views.proofreading_feed, name='Proofreading'),
  url(r'^feedUnpublished$', views.publishing_feed, name='Publishing' ),
  url('mydrafts/', views.mydrafts, name='mydrafts'),
  url(r'^feedUnread/assignEditor/(?P<id>\d+)/$', views.assignEditor, name='assignEditor'),
  url(r'^feedUnread/deleteEditor/(?P<id>\d+)/$', views.deleteEditor, name='deleteEditor'),
  url(r'^feedUnread/select_copyEditor/(?P<id>\d+)/$', views.select_copyEditor, name='select_copyeditor'),
  url('newContent/', views.newContent, name='newContent'),

]