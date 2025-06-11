from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('projects/', views.project_list, name='project_list'),
    path('projects/create/', views.create_project, name='create_project'),
    path('projects/<int:project_id>/', views.project_detail, name='project_detail'),
    path('projects/<int:project_id>/task/add/', views.create_task, name='create_task'),
    path('register/', views.register, name='register'),
    path('tasks/<int:task_id>/move/<str:new_status>/', views.move_task, name='move_task'),
    path('tasks/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('tasks/<int:task_id>/edit/', views.edit_task, name='edit_task'),

    path('tasks/<int:task_id>/update_status/', views.update_task_status, name='update_task_status'),

]