from django.urls import path
from task_manager.labels import views


urlpatterns = [
    path('', views.Index.as_view(), name='labels'),
    path('create/', views.Create.as_view(), name='label_create'),
    path('<int:pk>/update/', views.Update.as_view(), name='label_update'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='label_delete'),
]
