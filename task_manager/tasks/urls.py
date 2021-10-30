from django.urls import path
from task_manager.tasks import views


urlpatterns = [
    path('', views.Index.as_view(), name='tasks'),
    path('create/', views.Create.as_view(), name='task_create'),
    path('<int:pk>/update/', views.Update.as_view(), name='task_update'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='task_delete'),
]