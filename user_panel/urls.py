from django.urls import path
from .views import *

urlpatterns = [
    path('apps/', AppListView.as_view(), name='app-list'),
    path("tasks/", UserTasksListView.as_view(), name="user-tasks"),
    path("tasks/submit/", SubmitTaskView.as_view(), name="submit-task"),
    path('app/<int:pk>/', AppDetailView.as_view(), name='app-detail'),
    path('task/<int:pk>/', TaskDetailView.as_view(), name='task-detail'),

]