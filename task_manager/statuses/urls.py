from django.urls import path
from task_manager.statuses import views


urlpatterns = [
    path('', views.Index.as_view(), name='statuses'),
    path('create/', views.Create.as_view(), name='status_create'),
    path('<int:pk>/update/', views.Update.as_view(), name='status_update'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='status_delete'),
]