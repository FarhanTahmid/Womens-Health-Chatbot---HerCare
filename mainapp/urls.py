from django.urls import path
from . import views
from .views import ChatbotAPI
app_name = "mainapp"

urlpatterns = [
    path('',views.landingPage,name="landingPage"),
    path('chatbot',views.chatBox,name="chatbot"),
    path('chatbotAPI/',ChatbotAPI.as_view(),name='chatbotapi'),

    
]
