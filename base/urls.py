from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('create-room/', views.createRoom, name='create_room'),
    path('login/', views.loginPage, name='login_page'),
    path('logout/', views.logoutUser, name='logoutUser'),
    path('register/', views.userRegistration, name='user_registration'),
    path('room/<int:pk>/', views.room, name='room'),
    path('delete_room/<int:pk>/', views.deleteRoom, name='delete_room'),
    path('delete_message/<int:pk>/', views.deleteMessage, name='delete_message'),
]