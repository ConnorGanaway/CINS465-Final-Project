from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path('', views.index),
    path('useful/', views.delete_random),
    path('admin/', views.admin_view),
    path('login/', auth_views.LoginView.as_view()),
    path('register/', views.register_view),
    path('logout/', views.logout_view),
    path('community/<str:community_id>/', views.community_view),
    path('community/<str:community_id>/follow/', views.follow),
    path('community/<str:community_id>/unfollow/', views.unfollow),
    path('community/<str:community_id>/suggestion/', views.suggestion_view),
    path('community/<str:community_id>/suggestion/<int:sugg_id>/upvote/', views.upvote),
    path('community/<str:community_id>/suggestion/<int:sugg_id>/downvote/', views.downvote),
    path('suggestions/', views.suggestions_view),
    path('community/<str:community_id>/comment/<int:sugg_id>/', views.comment_view),
    path('cur_community/<str:community_id>/', views.cur_community_view),
    path('create_community/', views.create_community_view),
    path('profile/<str:name>/', views.profile_view),
    path('profile/<str:name>/update_picture/', views.update_profile_picture_view),
    path('profile/<str:name>/update_about/', views.update_profile_about_view),
    path('profile/<str:name_to_follow>/add_friend/<str:user_name>/', views.addFriend),
    path('profile/<str:name_to_remove>/remove_friend/<str:user_name>/', views.removeFriend),
    path('profile/<str:user_name_to_add>/accept_friend/<str:user_name>/', views.acceptFriendRequest),
    path('profile/<str:user_name_to_decline>/decline_friend/<str:user_name>/', views.declineFriendRequest),
    path('community/<str:room_name>/chat/', views.room, name='room'),
]
