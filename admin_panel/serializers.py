from rest_framework import serializers
from .models import App
from auth_system.models import AppUser

class AppSerializer(serializers.ModelSerializer):
    app_image = serializers.ImageField(required=True)  # Explicitly declare the image field

    class Meta:
        model = App
        fields = '__all__'  # Include all fields

    def create(self, validated_data):
        request = self.context.get("request")
        if request and hasattr(request, "user"):
            validated_data["created_by_id"] = request.user.id
            validated_data["created_by_name"] = request.user.get_full_name() or request.user.username
        return super().create(validated_data)
    
    def update(self, instance, validated_data):
        app_image = validated_data.pop("app_image", None)

        if app_image:
            if isinstance(app_image, str) and app_image.startswith("http"): 
                # If it's a Cloudinary URL, do not update
                pass
            else:
                # If it's a new file, update the image
                instance.app_image = app_image

        # Update other fields
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        
        instance.save()
        return instance

class AdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'is_admin']
        read_only_fields = ['id', 'role']

    def create(self, validated_data):
        validated_data['role'] = AppUser.ROLE_ADMIN
        validated_data['is_admin'] = True
        return super().create(validated_data)

