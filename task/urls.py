from django.urls import path,include
from .views import TaskListView,TaskDoneView
urlpatterns = [
    path('all/',TaskListView.as_view(),name='task-all'),
    path('create/',TaskListView.as_view(),name='task-create'),
    path('task-done/',TaskDoneView.as_view(),name='task-done')
]