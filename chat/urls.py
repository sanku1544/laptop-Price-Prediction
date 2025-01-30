from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns
    path('chat/', views.chat_with_gemini, name='chat_with_gemini'),
]
