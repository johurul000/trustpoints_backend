from django.urls import path
from .views import *

urlpatterns = [
    path('apps/', GetAllAppsView.as_view(), name='get-all-apps'),
    path('all-apps/', AllAppsView.as_view(), name='all-apps'),
    path('apps/add/', AddNewAppView.as_view(), name='add-app'),
    path('apps/<int:pk>/edit/', EditAppView.as_view(), name='edit-app'),
    path('apps/<int:pk>/delete/', DeleteAppView.as_view(), name='delete-app'),

    path('list-admins/', AdminListView.as_view(), name='admin-list'),
    path('create-admin/', AdminCreateView.as_view(), name='admin-create'),
    path('edit-admin/<int:pk>/', AdminUpdateView.as_view(), name='admin-update'),

    path('tasks/', AllTasksListView.as_view(), name='task-list'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-list'),
    path('tasks/<int:task_id>/verify/', VerifyTaskView.as_view(), name='verify_task'),
    path('tasks/<int:task_id>/reject/', RejectTaskView.as_view(), name='reject_task'),

]


