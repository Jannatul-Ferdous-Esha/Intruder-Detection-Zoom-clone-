from django.urls import path
from . import views

urlpatterns = [
    path('register/',views.register, name='register'),
    path('login/',views.login_view, name='login'),
    path('dashboard/',views.dashboard, name='dashboard'),
    path('meeting/',views.videocall, name='meeting'),
    path('logout/',views.logout_view, name='logout'),
    path('join/',views.join_room, name='join_room'),
    path('',views.index, name='index'),
    path('create-meeting/', views.create_meeting, name='create_meeting'),  
    path('capture_video/', views.capture_video, name='capture_video'),
    path('process_face/', views.process_face, name='process_face'),
    path('insider/', views.insider_view, name='insider'),
    path('intruder/', views.intruder_view, name='intruder'),
    path('capture_photo/', views.capture_photo, name='capture_photo'),

    

]
