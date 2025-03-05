from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.response import Response

from user_panel.models import Task
from user_panel.serializers import TaskSerializer
from .models import App
from .serializers import AppSerializer, AdminSerializer
from .permissions import IsCustomAdmin  # Import custom permission
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q
from rest_framework.views import APIView
from django.contrib.auth import get_user_model

AppUser = get_user_model()

# 🚀 Add New App
class AddNewAppView(generics.CreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]  # Use custom admin check

    def perform_create(self, serializer):
        serializer.save()

# Custom Pagination: 10 Apps Per Page
class AppPagination(PageNumberPagination):
    page_size = 10  # Default items per page
    page_size_query_param = "page_size"  # Allow dynamic page size (optional)
    max_page_size = 50  # Limit max items per page

class GetAllAppsView(generics.ListAPIView):
    serializer_class = AppSerializer
    permission_classes = [IsCustomAdmin]
    pagination_class = AppPagination

    def get_queryset(self):
        return App.objects.filter(is_deleted=False)

    def list(self, request, *args, **kwargs):
        response = super().list(request, *args, **kwargs)
        total_apps = App.objects.filter(is_deleted=False).count()  # Total apps count
        response.data["total_apps"] = total_apps  # Add total apps count to response
        return Response(response.data, status=status.HTTP_200_OK)
    
class AllAppsView(APIView):
    permission_classes = [IsCustomAdmin]

    def get(self, request):
        apps = App.objects.filter(is_deleted=False)
        
        apps_serializer = AppSerializer(apps, many=True)

        return Response(apps_serializer.data, status=status.HTTP_200_OK)
    

# 🚀 Edit App (Update by ID)
class EditAppView(generics.RetrieveUpdateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsCustomAdmin]

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        print("Incoming Data:", request.data)  # Debugging
        serializer = self.get_serializer(instance, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        
        print("Errors:", serializer.errors)  # Log errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# 🚀 Soft Delete App (Mark as Deleted)
class DeleteAppView(generics.DestroyAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsCustomAdmin]

    def destroy(self, request, *args, **kwargs):
        app = self.get_object()
        app.is_deleted = True  # Soft delete
        app.save()
        return Response({"message": "App deleted successfully"}, status=status.HTTP_204_NO_CONTENT)
    

    # Admins Managment

class AdminListView(generics.ListAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return AppUser.objects.filter(is_admin=True, is_superuser=False).exclude(id=self.request.user.id)


class AdminCreateView(generics.CreateAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsCustomAdmin]

class AdminUpdateView(generics.RetrieveUpdateAPIView):
    serializer_class = AdminSerializer
    permission_classes = [IsCustomAdmin]
    queryset = AppUser.objects.filter(is_admin=True)


# Verify task

class AllTasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsCustomAdmin]

    def get_queryset(self):
        return Task.objects.all()
    
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()  # Fetch Task objects, not App objects
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return Response(TaskSerializer(task).data)
    

class VerifyTaskView(generics.UpdateAPIView):
    """
    Verify a task, update its status, and add points to the user.
    """
    permission_classes = [IsCustomAdmin]
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['task_id'])

        if task.status != "pending":
            return Response({"error": "Task is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        # Update task status
        task.status = "verified"
        task.save()

        # Add points to the user (directly updating AppUser model)
        task.user.points += task.app.points  # Add the app's points to user's total
        task.user.save()

        return Response(
            {"message": "Task verified successfully", "new_points": task.user.points},
            status=status.HTTP_200_OK
        )
    
class RejectTaskView(generics.UpdateAPIView):
    """
    Reject a task without awarding points.
    """
    permission_classes = [IsCustomAdmin]
    serializer_class = TaskSerializer

    def update(self, request, *args, **kwargs):
        task = get_object_or_404(Task, id=kwargs['task_id'])

        if task.status != "pending":
            return Response({"error": "Task is not pending"}, status=status.HTTP_400_BAD_REQUEST)

        # Update task status
        task.status = "rejected"
        task.save()

        return Response({"message": "Task rejected successfully"}, status=status.HTTP_200_OK)
