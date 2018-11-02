from django.conf.urls import url
from . import views

app_name = 'accounts'

urlpatterns = [
    url(r'^signup/$',views.signup_view, name="signup"),
    url(r'^login/$',views.login_view, name="login"),
    url(r'^logout/$',views.logout_view, name="logout"),
    url(r'^profile/$',views.profile, name="profile"),
    url(r'^profile/edit/$',views.edit_profile, name="edit_profile"),
    url(r'^profile/edit/2/(?P<id>\d+)/$',views.edit_userprofile, name="edit_userprofile"),
    url(r'^change-password/$',views.change_password, name="change_password"),

]