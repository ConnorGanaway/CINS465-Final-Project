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
    path('community/<str:room_name>/chat/', views.room, name='room'),
]
