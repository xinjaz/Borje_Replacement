from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm  # Make sure this form exists

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')  # Redirect to the dashboard after registration
    else:
        form = UserRegistrationForm()
    return render(request, 'quotes/register.html', {'form': form})

def dashboard(request):
    # Render the dashboard template
    return render(request, 'quotes/dashboard.html')
def home(request):
    return render(request, 'quotes/home.html')
