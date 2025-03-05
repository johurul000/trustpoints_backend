from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class AppUser(AbstractUser):
    ROLE_ADMIN = 'admin'
    ROLE_USER = 'user'

    ROLE_CHOICES = [
        (ROLE_ADMIN, 'Admin'),
        (ROLE_USER, 'User'),
    ]

    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_USER)
    points = models.PositiveIntegerField(default=0)  # Track earned points
    is_admin = models.BooleanField(default=False)  # Easier admin checks

    # Custom related_name for groups & permissions to avoid conflicts
    groups = models.ManyToManyField(
        Group,
        related_name='appuser_set',
        blank=True,
        help_text='The groups this user belongs to.'
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name='appuser_permissions_set',
        blank=True,
        help_text='Specific permissions for this user.'
    )

    def save(self, *args, **kwargs):
        # Ensure superusers are always admins
        if self.is_superuser:
            self.role = self.ROLE_ADMIN
            self.is_admin = True
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"
