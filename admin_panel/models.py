from django.db import models
from cloudinary.models import CloudinaryField
from django.contrib.auth import get_user_model

User = get_user_model()

class App(models.Model):
    name = models.CharField(max_length=255, unique=True)
    app_link = models.CharField(max_length=255, unique=True)  # e.g., com.facebook.katana
    app_category = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    points = models.PositiveIntegerField()
    app_image = CloudinaryField('image')

    # Soft deletion
    is_deleted = models.BooleanField(default=False)

    # Admin details (soft reference, not a ForeignKey)
    created_by_id = models.PositiveIntegerField(null=True, blank=True)  # Store the admin's user ID
    created_by_name = models.CharField(max_length=255, null=True, blank=True)  # Store the admin's name

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    def soft_delete(self):
        """Marks the app as deleted instead of actually deleting it."""
        self.is_deleted = True
        self.save()
