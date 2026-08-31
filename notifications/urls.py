# notifications/urls.py
from django.urls import path
from . import views

app_name = "notifications"  # <-- must be here

urlpatterns = [
    path("", views.notification_list, name="notification_list"),
    path("mark-read/<int:pk>/", views.mark_notification_read, name="mark_notification_read"),
    path("delete/<int:pk>/", views.delete_notification, name="delete_notification"),
    path("mark-all-read/", views.mark_all_read, name="mark_all_read"),
    path("count/", views.notification_count, name="notification_count"),
]