from django.urls import path
from . import views

urlpatterns = [
    path('my-chats/', views.chat_list, name='chat_list'),
    path('<int:chat_id>/', views.chat_view, name='chat_view'),
    path('chat/create/<int:id>/<str:mode>/', views.create_chat, name='create_chat'),

]
