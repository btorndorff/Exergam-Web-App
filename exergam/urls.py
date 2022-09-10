from django.urls import path
from django.contrib.auth.views import LogoutView

from . import views
app_name = 'exergam'

urlpatterns = [ 
    path('logout', LogoutView.as_view(), name='logout'),
    path('', views.FeedView.as_view(), name='load'),
    path('home', views.HomeView.as_view(), name='home'),
    path('<int:pk>/profile', views.ProfileView.as_view(), name='profile'),
    path('userupdate', views.UserUpdateView.as_view(), name='edit'),
    path('feed', views.FeedView.as_view(), name='feed'),
    path('newentry', views.newentry, name='entry'),
    path('upload', views.add_entries, name='upload'),
    path('leaderboard', views.LeaderboardView.as_view(), name='leaderboard'),
    path('myleaderboard', views.MyLeaderboardView.as_view(), name='myleaderboard'),
    path('<int:follow_id>/follow', views.follow, name='follow'),
    path('location', views.location_option, name='location_option'),
    path('select_location', views.LocationView.as_view(), name='select_location'),
    path('newpost/<int:location_id>', views.newpost, name='new_post'),
    path('post', views.add_post, name='post'),
    path('comment/<int:post_id>', views.comment_on_other, name='comment'),
    path('commentown/<int:post_id>', views.comment_on_own, name='comment_own'),
    path('search', views.search, name='search'),
    path('find', views.SearchView.as_view(), name='find'),
    path('<int:unfollow_id>/unfollow', views.unfollow, name='unfollow')
]