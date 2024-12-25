from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register),
    path('login/', views.login_view),
    path('logout/', views.logout_view),
    path('employees/', views.employee_list),
    path('employees/<int:pk>/', views.employee_detail),
    path('ideas/', views.idea_list),
    path('ideas/<int:pk>/', views.idea_detail),
    path('votes/', views.vote_list),
    path('votes/<int:pk>/', views.vote_detail),
    path('collaborations/', views.collaboration_list),
    path('collaborations/<int:pk>/', views.collaboration_detail),
    path('rewards/', views.reward_list),
    path('rewards/<int:pk>/', views.reward_detail),
]