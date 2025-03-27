from django.urls import path
from .views import *
from django.contrib.auth import views as auth_views
# django.contrib.auth import views as auth_views
# .LoginView.as_view(),registration/

urlpatterns = [
    path('',task_list,name='list'),
    path('signup',signup_view,name='signup'),
    path('login',login_view,name='login'),
    path('logout',logout_view,name='logout'),
    path('task/<int:pk>',task_detail,name='detail'),
    path('task/<int:pk>/edit',update_task,name='update'),
    path('task/<int:pk>/delete',delete_task,name='delete'),
    path('task/<int:pk>/toggle',toggle_task,name='toggle'),
    path('task/new/',create_task,name='create'),
]
