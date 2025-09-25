from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    path('chat/', views.chat_view, name='chat'),
    path('chat/<int:conversation_id>/', views.chat_view, name='chat_detail'),
    path('new-chat/', views.new_chat, name='new_chat'),
    path('send-message/', views.send_message, name='send_message'),
    path('get-conversations/', views.get_conversations, name='get_conversations'),
]