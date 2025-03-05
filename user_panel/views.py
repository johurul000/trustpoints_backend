from rest_framework import generics, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser
from .models import App, Task
from .serializers import AppSerializer, TaskSerializer

class AppListView(APIView):
    """
    API View to fetch all available apps (excluding soft-deleted ones).
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        apps = App.objects.filter(is_deleted=False)
        
        apps_serializer = AppSerializer(apps, many=True)

        return Response(apps_serializer.data, status=status.HTTP_200_OK)


class UserTasksListView(generics.ListAPIView):
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Task.objects.filter(user=self.request.user)

class AppDetailView(generics.RetrieveAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        app = self.get_object()
        return Response(AppSerializer(app).data)
    
class SubmitTaskView(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = (MultiPartParser, FormParser)  # Allows handling image uploads

    def post(self, request, *args, **kwargs):
        app_id = request.data.get("app")
        screenshot = request.data.get("screenshot")

        if not app_id:
            return Response({"error": "App ID is required"}, status=400)
        if not screenshot:
            return Response({"error": "Screenshot is required"}, status=400)

        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return Response({"error": "App not found"}, status=404)

        # Check if a task already exists (Pending or Verified)
        existing_task = Task.objects.filter(user=request.user, app=app).exclude(status="rejected").first()
        if existing_task:
            return Response({"error": "You have already submitted a task for this app."}, status=400)

        # Create a new task
        task = Task.objects.create(user=request.user, app=app, screenshot=screenshot)

        return Response(TaskSerializer(task).data, status=201)
    
class TaskDetailView(generics.RetrieveAPIView):
    queryset = Task.objects.all()  # Fetch Task objects, not App objects
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        task = self.get_object()
        return Response(TaskSerializer(task).data) 
    


# Profile management.




