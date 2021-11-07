from django.urls import path
from task_manager.users import views


urlpatterns = [
    path('', views.Index.as_view(), name='users'),
    path('create/', views.Create.as_view(), name='create'),
    path('<int:pk>/update/', views.Update.as_view(), name='update'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='delete'),
]
