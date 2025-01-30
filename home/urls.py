from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),    
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('contact_form/', views.contact_form, name='contact_form'),  # Fix here, use a unique name
    path('profile/', views.profile, name='profile'),
    path('ppredict/', views.ppredict, name='ppredict'),
    path('predict2/', views.predict2, name='predict2'),
    path('feedback/', views.feedback, name='feedback'),
    path('feedback_form/', views.feedback_form, name='feedback_form'),

]



  # Add this line for registration
