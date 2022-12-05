from django.contrib import admin
from django.urls import path,include
from .views import Tasklist,Taskdetail,taskcreate,taskupdate,taskdelete,userlogin,userregistration
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login/',userlogin.as_view(),name="login"), 
    path('register/',userregistration.as_view(),name="register"), 
    path('',Tasklist.as_view(),name="index"),
    path('task/<int:pk>/',Taskdetail.as_view(),name="task"),
    path('taskcreate',taskcreate.as_view(),name="taskcreate"),
    path('taskupdate/<int:pk>/',taskupdate.as_view(),name="taskupdate"),
    path('taskdelete/<int:pk>/',taskdelete.as_view(),name="taskdelete"),
    path('logout/',LogoutView.as_view(next_page='login') ,name="logout"),

]
