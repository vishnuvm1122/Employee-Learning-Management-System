from django.urls import path
from . import views


urlpatterns = [
    # ---------------- Create / Assign Courses ----------------
    # path(
    #     "allocate/", 
    #     views.course_allocation_create, 
    #     name="course_allocation_create"
    # ),

    # ---------------- List / Filter Allocations ----------------
    path(
        "allocated/", 
        views.CourseAllocationListView.as_view(), 
        name="course_allocation_view"
    ),

    # ---------------- Edit Allocation ----------------
    # path(
    #     "edit/<int:pk>/", 
    #     views.edit_allocated_course, 
    #     name="edit_allocated_course"
    # ),

    # ---------------- Deallocate Courses ----------------
    # path(
    #     "deallocate/<int:pk>/", 
    #     views.deallocate_course, 
    #     name="course_deallocate"
    # ),
]