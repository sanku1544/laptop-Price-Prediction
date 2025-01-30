from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),  # This will handle home/ URLs)
    path('', include('chat.urls')),  # This will handle chat/ URLs)
    path('predictor', include('predictor.urls')), 
    path('accounts/', include('accounts.urls')),  # This will handle predictor/ URLs
    path('accounts/', include('allauth.urls')),  # This will handle predictor/ URLs
    
  # This will handle predictor/ URLs
 # This will handle predictor/ URLs
]
