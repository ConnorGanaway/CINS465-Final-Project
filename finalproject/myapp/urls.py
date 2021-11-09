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
    path('suggestions/', views.suggestions_view),
    path('suggestion/', views.suggestion_view),
    path('comment/<int:sugg_id>/', views.comment_view),
    path('community/<int:community_id>/', views.community_view),
]
