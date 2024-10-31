
from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class ProjectQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2)
    markup = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name

class Material(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    unit = models.CharField(max_length=50)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

# Project Table
class Project(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Approved', 'Approved'),
        ('Completed', 'Completed'),
        ('Rejected', 'Rejected')
    ]

    name = models.CharField(max_length=100)
    description = models.TextField()
    startDate = models.DateTimeField(null=True, blank=True)
    endDate = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    approved_by_admin = models.BooleanField(default=False)
    approved_by_user = models.BooleanField(default=False)
    declined_by_admin = models.BooleanField(default=False)
    declined_by_user = models.BooleanField(default=False)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if self.status == 'Approved' and not self.startDate:
            self.startDate = timezone.now()
        if self.status == 'Completed' and not self.endDate:
            self.endDate = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Pricing Table
class Pricing(models.Model):
    price = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField(auto_now_add=True)
    materials = models.ForeignKey(Material, on_delete=models.CASCADE)
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.project.name} - {self.materials.name}"

# Project Element Table
class ProjectElement(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    createdAt = models.DateTimeField(auto_now_add=True)
    updatedAt = models.DateTimeField(auto_now=True)

    ELEMENT_CHOICES = [
        ('Framing', 'Framing'),
        ('Window and Door Installation', 'Window and Door Installation'),
        ('Electrical', 'Electrical'),
        ('Plumbing', 'Plumbing'),
    ]
    element_type = models.CharField(max_length=100, choices=ELEMENT_CHOICES)

    def __str__(self):
        return f"{self.project.name} - {self.element_type}"
