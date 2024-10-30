# project_quotes/urls.py

from django.contrib import admin
from django.urls import path, include
from quotes.views import register, home  # Import your views here

urlpatterns = [
    path('admin/', admin.site.urls),
    path('quotes/', include('quotes.urls')),  # Make sure to add a trailing slash here
    path('register/', register, name='register'),  # Register route
    path('', home, name='home'),  # Home route
]
