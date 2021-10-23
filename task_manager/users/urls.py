from django.contrib import admin
from django.urls import path, include
from task_manager.users import views
from django.conf.urls.i18n import i18n_patterns
from django.utils.translation import gettext_lazy as _


urlpatterns = [
    path('', views.Index.as_view(), name='users'),
    path('create/', views.Create.as_view(), name='create'),
    path('<int:pk>/update/', views.Update.as_view(), name='update'),
    path('<int:pk>/delete/', views.Delete.as_view(), name='delete'),
]
