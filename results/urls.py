from django.urls import path
from . import views



urlpatterns = [
    path('result', views.ResultView.as_view(), name="result"),
    path("certificate/<int:user_id>/<int:course_id>/",views.download_certificate,name="download_certificate"),
  

]




