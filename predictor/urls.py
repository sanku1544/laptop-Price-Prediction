from django.urls import path
from . import views

app_name = 'predictor'

urlpatterns = [
    path('', views.predictor, name='home'),
    path('allinone/', views.allinone, name='allinone'),
    path('predict/', views.predict_price, name='predict_price'),

    

  # Add this line for registration
]
