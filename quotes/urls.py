# quotes/urls.py

from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),  # Route for user registration
    path('login/', LoginView.as_view(template_name='quotes/login.html'), name='login'),  # Route for user login
    path('logout/', LogoutView.as_view(), name='logout'),  # Route for user logout# Default route for the dashboard
    path('', views.dashboard, name='dashboard'),
]
