from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskListView.as_view(), name='task_list_url'),
    path('<int:id>/', TaskDetailView.as_view(), name='task_detail_url'),
    path('<int:id>/accept/', TaskDetailView.accept, name='task_update_url'),
    path('create/', TaskCreateView.as_view(), name='task_create_url'),
]
