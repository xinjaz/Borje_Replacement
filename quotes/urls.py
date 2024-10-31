from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from . import views
from .views import materials, add_material, edit_material, delete_material, request_quote

urlpatterns = [
    path('register/', views.register, name='register'),  # Route for user registration
    path('login/', LoginView.as_view(template_name='quotes/login.html'), name='login'),  # Route for user login
    path('logout/', LogoutView.as_view(), name='logout'),  # Route for user logout
    path('quotes/', views.dashboard, name='dashboard'),  # Route for dashboard
    path('project/<int:project_id>/materials/', materials, name='materials'),
    path('project/<int:project_id>/materials/add/', add_material, name='add_material'),
    path('materials/edit/<int:material_id>/', edit_material, name='edit_material'),
    path('materials/delete/<int:material_id>/', delete_material, name='delete_material'),
]
