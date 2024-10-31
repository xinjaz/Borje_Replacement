from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from .forms import UserRegistrationForm  # Make sure this form exists
from .models import Project
from .forms import QuoteRequestForm
from django.core.mail import send_mail

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
    projects = Project.objects.all()  # Fetch all projects
    materials = Material.objects.all()  # Fetch all materials (or filter by project if needed)

    context = {
        'projects': projects,
        'materials': materials,  # You can modify this if you want to show materials related to a specific project
    }

    return render(request, 'quotes/dashboard.html', {'project': projects})

def home(request):
    return render(request, 'quotes/home.html')

def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = 'Approved'
    project.approved_by_admin = True
    project.startDate = timezone.now()
    project.save()
    return redirect('dashboard')

from .models import Material, Project
def materials(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    materials = Material.objects.all()  # Adjust this query if you want to filter by project
    return render(request, 'materials.html', {'materials': materials, 'project': project})

def add_material(request, project_id):
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        unit = request.POST['unit']
        Material.objects.create(name=name, description=description, unit=unit)
        return redirect('materials', project_id=project_id)
    return render(request, 'add_material.html', {'project_id': project_id})

def edit_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.name = request.POST['name']
        material.description = request.POST['description']
        material.unit = request.POST['unit']
        material.save()
        return redirect('materials', project_id=material.project.id)
    return render(request, 'edit_material.html', {'material': material})

def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    project_id = material.project.id
    material.delete()
    return redirect('materials', project_id=project_id)


def request_quote(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            # Process the form data
            name = form.cleaned_data['name']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            description = form.cleaned_data['description']
            materials_needed = form.cleaned_data['materials_needed']

            # Here you can save the data to the database or send an email
            # Example: send a confirmation email (requires proper email setup)
            send_mail(
                'Quote Request Received',
                f'Name: {name}\nEmail: {email}\nPhone: {phone}\nDescription: {description}\nMaterials: {materials_needed}',
                'from@example.com',  # Replace with your email
                [email],
                fail_silently=False,
            )

            return redirect('quote_success')  # Redirect to a success page or back to the form

    else:
        form = QuoteRequestForm()

    return render(request, 'quotes/request_quote.html', {'form': form})

def quote_success(request):
    return render(request, 'quotes/quote_success.html')