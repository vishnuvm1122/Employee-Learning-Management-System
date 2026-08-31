from django.urls import path
from . import views

urlpatterns = [

    # ========================
    # Program URLs
    # ========================
    path("", views.ProgramFilterView.as_view(), name="programs"),
    path("<int:pk>/detail/", views.program_detail, name="program_detail"),
    path("add/", views.program_add, name="add_program"),
    path("<int:pk>/edit/", views.program_edit, name="edit_program"),
    path("<int:pk>/delete/", views.program_delete, name="program_delete"),

    # ========================
    # Course URLs 
    # ========================
    path("course/<pk>/detail/", views.course_details, name="course_details"),
    path("<int:pk>/course/add/", views.course_add, name="course_add"),
    path("course/<pk>/edit/", views.course_edit, name="edit_course"),
    path("course/delete/<pk>/", views.course_delete, name="course_delete"),
    
    
    # ========================
    # Video URLs 
    # ========================
    
    path("<int:pk>/video/add/", views.course_video_upload, name="course_video_upload"),
    path("<int:pk>/video/<int:video_id>/edit/", views.course_video_edit, name="course_video_edit"),
    path("<int:pk>/video/<int:video_id>/delete/", views.course_video_delete, name="course_video_delete"),
    

    # ================= FILE UPLOAD =================
    
    path("<int:pk>/file/add/",views.course_file_upload,name="course_file_upload"),
    path( "<int:pk>/file/<int:file_id>/edit/", views.course_file_edit,name="course_file_edit"),
    path( "<int:pk>/file/<int:file_id>/delete/",views.course_file_delete,name="course_file_delete"),
    
    
    # ========================
    #  Watch Video URLs 
    # ========================
    
    path('course/<int:course_id>/video/<int:video_id>/', views.handle_video_single, name='video_single'),
    path('course/<int:course_id>/video/<int:video_id>/played/', views.video_played, name='video_played'),
    
    # ========================
    #  request_course_access 
    # ========================

    path('course/request-access/<int:course_id>/', views.request_course_access, name='request_course_access'),


]

    # Course urls
