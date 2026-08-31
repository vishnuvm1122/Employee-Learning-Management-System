from django.urls import path
from . import views

urlpatterns = [
    path("latest/", views.latest_version, name="latest_version"),
    path("download/<int:pk>/", views.download_apk, name="download_apk"),
]