from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('send', views.send, name='send'),
    path('chat', views.chat, name='chat'),
    path('js_chat_hist', views.jsChatHist, name='jsChatHist'),
    path('js_chat_send', views.jsChatSend, name='jsChatSend'),
]