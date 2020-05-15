from django.urls import path
from django.conf.urls import url
from django.contrib.auth import views as auth_views


from . import views

urlpatterns = [
    path('Register', views.registration_view, name='Register'),
    path('', views.home, name='home'),
    path('login', views.login1, name='login'),
    path('recently_added', views.vid, name='recently_added'),
    path('upload', views.showimage, name='upload'),
     path('like_dislike', views.LikePost, name='like_dislike_post'),
    path('readmore/<str:videoid>', views.readmore, name='readmore'),
    path('post/<str:videoid>', views.post, name='post'),
    path('logout', views.logout1, name='logout'),
    path('profile', views.profile, name='profile'),
     path('socialLogin', views.socialLogin, name='socialLogin'),
    path('triple', views.triple, name='triple'),
    path('trending', views.trending, name='trending'),
    path('User_Profile/<str:username>', views.User_Profile, name='User_Profile'),
    path('duet', views.duet, name='duet'),
    url(r'^profile/pricing/$', views.pricing, name='pricing'),
    path('celeb', views.celeb, name='celeb'),
    url(r'^profile/edit/$', views.edit_profile, name='edit_profile'),
    url(r'^profile/password/$', views.change_password, name='change_password'),

    url(r'^password_reset/$', auth_views.PasswordResetView.as_view(), name='password_reset'),
    url(r'^password_reset/done/$', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    url(r'^reset/done/$', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]
