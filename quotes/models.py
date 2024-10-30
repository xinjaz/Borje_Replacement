
from django.db import models
from django.contrib.auth.models import User

class ProjectQuote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    project_name = models.CharField(max_length=100)
    material_cost = models.DecimalField(max_digits=10, decimal_places=2)
    markup = models.DecimalField(max_digits=5, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.project_name
