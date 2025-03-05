from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model
from admin_panel.models import App

User = get_user_model()

class Task(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('submitted', 'Submitted'),
        ('verified', 'Verified'),
        ('rejected', 'Rejected'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    screenshot = CloudinaryField('screenshot', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username} - {self.app.name} ({self.status})"
    
class UserPoints(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.PositiveIntegerField(default=0)

    def __str__(self):
        return f"{self.user.username} - {self.total_points} Points"

