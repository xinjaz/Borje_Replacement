from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.utils import timezone
from django.core.mail import send_mail
from .forms import UserRegistrationForm, QuoteRequestForm  # Ensure these forms are defined in your forms.py
from .models import Project, Material, ProjectElement
from django.http import HttpResponse

projects= []
def request_quote(request):
    if request.method == 'POST':
        form = QuoteRequestForm(request.POST)
        if form.is_valid():
            area_size = form.cleaned_data['area_size']
            project_element = form.cleaned_data['project_element']
            material = form.cleaned_data['material']

            # Create the project quotation for the user
            project = Project.objects.create(
                user=request.user,
                name="New Project",
                description="Project requested by user",
                area_size=area_size,
                status="Pending",
            )
            ProjectElement.objects.create(project=project, element_type=project_element, material=material)

            return redirect('home')
    else:
        form = QuoteRequestForm()

    materials = Material.objects.all()
    project_elements = ProjectElement.objects.values_list('element_type', flat=True).distinct()

    context = {
        'form': form,
        'materials': materials,
        'project_elements': project_elements,
    }
    return render(request, 'quotes/request_quote.html', context)

def submit_quotation(request):
    if request.method == 'POST':
        area_size = request.POST.get('areaSize')
        project_element = request.POST.get('projectElement')
        material = request.POST.get('material')

        project = {
            'id': len(request.session.get('projects', [])) + 1,
            'description': f'{material} for {project_element} covering {area_size} sq.m',
            'location': 'Sample Location',  # Modify as necessary
            'status': 'Pending',
        }

        if 'projects' not in request.session:
            request.session['projects'] = []
        request.session['projects'].append(project)
        request.session.modified = True  # Mark the session as modified

        # Debug: Print the current session projects
        print("Current session projects:", request.session['projects'])  # Check if projects are stored correctly

        return redirect('dashboard')  # Redirect to the dashboard
    return HttpResponse(status=400)  # Return a bad request for non-POST

def dashboard(request):
    projects = request.session.get('projects', [])
    print("Projects in session:", projects)  # Debugging output to check session data
    return render(request, 'dashboard.html', {'project_list': projects})

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('dashboard')
    else:
        form = UserRegistrationForm()
    return render(request, 'quotes/register.html', {'form': form})


def dashboard(request):
    projects = Project.objects.all()  # Fetch all projects
    materials = Material.objects.all()  # Fetch all materials

    context = {
        'projects': projects,
        'materials': materials,  # Adjust if you want to filter materials for specific projects
    }

    return render(request, 'quotes/dashboard.html', context)


def home(request):
    return render(request, 'quotes/home.html')


def approve_project(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    project.status = 'Approved'
    project.approved_by_admin = True
    project.startDate = timezone.now()
    project.save()
    return redirect('dashboard')


def materials(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    # Filter materials by project if the Material model has a relationship with Project
    materials = Material.objects.filter(project=project) if hasattr(Material, 'project') else Material.objects.all()
    return render(request, 'quotes/materials.html', {'materials': materials, 'project': project})


def add_material(request, project_id):
    project = get_object_or_404(Project, id=project_id)
    if request.method == 'POST':
        name = request.POST['name']
        description = request.POST['description']
        unit = request.POST['unit']
        # Link the material to the project if the Material model has a ForeignKey to Project
        Material.objects.create(name=name, description=description, unit=unit, project=project)
        return redirect('materials', project_id=project_id)
    return render(request, 'quotes/add_material.html', {'project_id': project_id})


def edit_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    if request.method == 'POST':
        material.name = request.POST['name']
        material.description = request.POST['description']
        material.unit = request.POST['unit']
        material.save()
        # Redirect based on whether the Material model has a ForeignKey to Project
        return redirect('materials', project_id=material.project.id) if hasattr(material, 'project') else redirect('dashboard')
    return render(request, 'quotes/edit_material.html', {'material': material})


def delete_material(request, material_id):
    material = get_object_or_404(Material, id=material_id)
    project_id = material.project.id if hasattr(material, 'project') else None
    material.delete()
    # Redirect appropriately based on project association
    if project_id:
        return redirect('materials', project_id=project_id)
    return redirect('dashboard')




def quote_success(request):
    return render(request, 'quotes/quote_success.html')


