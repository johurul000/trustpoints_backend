from rest_framework import serializers
from admin_panel.models import App
import cloudinary.utils  # Import Cloudinary utilities
from .models import Task

class AppSerializer(serializers.ModelSerializer):
    app_image = serializers.SerializerMethodField()  # Override app_image

    class Meta:
        model = App
        fields = '__all__'  # Return all fields

    def get_app_image(self, obj):
        """Returns the full Cloudinary URL"""
        if obj.app_image:
            return cloudinary.utils.cloudinary_url(obj.app_image.public_id)[0]
        return None  # Return None if no image is uploaded
    
class TaskSerializer(serializers.ModelSerializer):
    app_name = serializers.CharField(source="app.name", read_only=True)
    app_image = serializers.ImageField(source="app.app_image", read_only=True)  # Returns full URL
    screenshot = serializers.SerializerMethodField()  # Ensure full Cloudinary URL
    username = serializers.CharField(source="user.username", read_only=True)
    email = serializers.EmailField(source="user.email", read_only=True)

    class Meta:
        model = Task
        fields = ["id", "app", "app_name", "app_image", "status", "screenshot", "created_at",  "username", "email"]
        read_only_fields = ["status", "created_at"]

    def get_screenshot(self, obj):
        if obj.screenshot:
            return obj.screenshot.url  # Return Cloudinary full URL
        return None
        
