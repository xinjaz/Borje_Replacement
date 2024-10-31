from django.contrib import admin
from .models import Material, Project, Pricing, ProjectElement

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ('name', 'unit', 'createdAt', 'updatedAt')

@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'user', 'approved_by_admin', 'approved_by_user', 'createdAt', 'updatedAt')
    list_filter = ('status', 'approved_by_admin', 'approved_by_user')

@admin.register(Pricing)
class PricingAdmin(admin.ModelAdmin):
    list_display = ('price', 'date', 'materials', 'project', 'createdAt', 'updatedAt')

@admin.register(ProjectElement)
class ProjectElementAdmin(admin.ModelAdmin):
    list_display = ('project', 'element_type', 'createdAt', 'updatedAt')
    list_filter = ('element_type',)