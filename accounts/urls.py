from django.urls import path
from . import views

app_name = 'accounts'  # This defines the namespace

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('update-profile/', views.update_profile, name='update_profile'),
    path('forgot_password/', views.forgot_password, name='forgot_password'),
    path('verify_otp/', views.verify_otp, name='verify_otp'),
    path("subscribe/", views.subscribe, name="subscribe"),
]




    # path('update_profile/', views.update_profile_view, name='update_profile'),
    # path('change_password/', views.change_password_view, name='change_password'),
    # path('delete_account/', views.delete_account_view, name='delete_account'),

