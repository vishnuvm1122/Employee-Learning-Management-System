from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from .models import CourseAllocation
from .forms import *
from course.models import Course, CourseVideo, VideoWatchProgress
from django.db.models import Sum
from django.shortcuts import redirect

from django.utils import timezone
from emailsettings.models import *
from emailsettings.utils import *
from notifications.models import Notification
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import ListView

# ---------------- CREATE / ASSIGN COURSES ----------------

User = get_user_model()



# @login_required
# def course_allocation_create(request):
#     if request.method == "POST":
#         form = CourseAllocationCreateForm(request.POST)

#         if form.is_valid():
#             employees = form.cleaned_data.get("employees")
#             selected_courses = form.cleaned_data.get("courses")

#             if not employees:
#                 messages.error(request, "Please select at least one employee.")
#                 return redirect("course_allocation_view")

#             if not selected_courses:
#                 messages.error(request, "Please select at least one course.")
#                 return redirect("course_allocation_view")

#             for employee in employees:
#                 allocation, created = CourseAllocation.objects.get_or_create(employee=employee)

#                 # ✅ OLD COURSES
#                 old_courses = set(allocation.courses.all())

#                 # ✅ ADD new courses (DON'T REMOVE OLD)
#                 allocation.courses.add(*selected_courses)

#                 # ✅ NEWLY ADDED COURSES ONLY
#                 new_courses = set(selected_courses) - old_courses

#                 # -----------------------------
#                 # 🔔 Notifications (ONLY NEW)
#                 # -----------------------------
#                 if new_courses:
#                     notifications = [
#                         Notification(
#                             sender=request.user,
#                             receiver=employee,
#                             message=f"You have been assigned to the course: {course.title}"
#                         )
#                         for course in new_courses
#                     ]
#                     Notification.objects.bulk_create(notifications)

#                 # -----------------------------
#                 # 📧 Email (ONLY NEW)
#                 # -----------------------------
#                 if employee.email and new_courses:
#                     for course in new_courses:
#                         html_message = render_to_string(
#                             "emails/course_assigned.html",
#                             {
#                                 "user": employee,
#                                 "course": course,
#                                 "assigned_by": request.user,
#                                 "course_link": request.build_absolute_uri(course.get_absolute_url()),
#                                 "now": timezone.now(),
#                             }
#                         )

#                         send_mail_notification(
#                             to_emails=[employee.email],
#                             subject=f"New Course Assigned: {course.title}",
#                             body=f"You have been assigned to {course.title}",
#                             html_message=html_message,
#                             request=request
#                         )

#             # -----------------------------
#             # 📧 Admin Email
#             # -----------------------------
#             notification_record = SendEmailToReceiveUsers.objects.first()

#             if notification_record:
#                 admin_users = notification_record.users.filter(email__isnull=False)
#             else:
#                 admin_users = User.objects.filter(is_superuser=True, email__isnull=False)

#             admin_emails = [user.email for user in admin_users if user.email]

#             if admin_emails:
#                 send_mail_notification(
#                     to_emails=admin_emails,
#                     subject="Course Allocation Completed",
#                     body=f"{', '.join([emp.get_full_name for emp in employees])} "
#                          f"have been assigned new course(s).",
#                     request=request
#                 )

#             messages.success(request, "Courses added successfully without removing old ones.")
#             return redirect("course_allocation_view")

#     else:
#         form = CourseAllocationCreateForm()

#     return render(request, "courseallocation/course_allocation_form.html", {
#         "form": form,
#         "title": "Assign Courses",
#     })


# # ---------------- EDIT ALLOCATION ----------------


# @login_required
# def edit_allocated_course(request, pk):
#     allocation = get_object_or_404(CourseAllocation, pk=pk)

#     # ✅ Store old courses BEFORE update
#     old_courses = set(allocation.courses.all())

#     if request.method == "POST":
#         form = CourseAllocationEditForm(request.POST, instance=allocation)

#         if form.is_valid():

#             # ✅ Save allocation (employee preserved via form clean method)
#             allocation = form.save()

#             # ✅ Update courses
#             new_courses = set(form.cleaned_data.get("courses", []))
#             allocation.courses.set(new_courses)

#             # =============================
#             # 🔍 FIND CHANGES
#             # =============================
#             added_courses = new_courses - old_courses
#             removed_courses = old_courses - new_courses

#             if added_courses or removed_courses:

#                 # =============================
#                 # 🔔 IN-APP NOTIFICATION
#                 # =============================
#                 message = "Your course allocation has been updated."

#                 if added_courses:
#                     message += "\nAdded: " + ", ".join(c.title for c in added_courses)

#                 if removed_courses:
#                     message += "\nRemoved: " + ", ".join(c.title for c in removed_courses)

#                 Notification.objects.create(
#                     sender=request.user,
#                     receiver=allocation.employee,
#                     message=message
#                 )

#                 # =============================
#                 # 📧 EMAIL TO EMPLOYEE
#                 # =============================
#                 if allocation.employee and allocation.employee.email:
#                     html_message = render_to_string(
#                         "emails/course_updated.html",
#                         {
#                             "user": allocation.employee,
#                             "added_courses": added_courses,
#                             "removed_courses": removed_courses,
#                             "updated_by": request.user,
#                             "now": timezone.now(),
#                         }
#                     )

#                     send_mail_notification(
#                         to_emails=[allocation.employee.email],
#                         subject="Course Allocation Updated",
#                         body="Your course allocation has been updated.",
#                         html_message=html_message,
#                         request=request
#                     )

#                 # =============================
#                 # 📧 EMAIL TO ADMINS
#                 # =============================
#                 notification_record = SendEmailToReceiveUsers.objects.first()

#                 if notification_record:
#                     admin_users = notification_record.users.filter(email__isnull=False)
#                 else:
#                     admin_users = User.objects.filter(is_superuser=True).exclude(email="")

#                 admin_emails = [u.email for u in admin_users if u.email]

#                 if admin_emails:
#                     send_mail_notification(
#                         to_emails=admin_emails,
#                         subject="Course Allocation Updated",
#                         body=f"{allocation.employee.get_full_name} course allocation updated.",
#                         request=request
#                     )

#             # =============================
#             # ✅ SUCCESS MESSAGE
#             # =============================
#             messages.success(request, "Course allocation updated successfully.")
#             return redirect("course_allocation_view")

#         else:
#             messages.error(request, "Please correct the errors below.")

#     else:
#         form = CourseAllocationEditForm(instance=allocation)

#     return render(
#         request,
#         "courseallocation/course_allocation_edit_form.html",
#         {
#             "form": form,
#             "title": "Edit Course Allocation",
#             "allocation": allocation,
#         }
#     )



#---------------- LIST / FILTER ALLOCATIONS ----------------

@method_decorator(login_required, name="dispatch")
class CourseAllocationListView(LoginRequiredMixin, ListView):

    model = CourseAllocation
    template_name = "courseallocation/course_allocation_view.html"
    context_object_name = "allocations"

    def get_queryset(self):

        queryset = (
            CourseAllocation.objects
            .select_related("employee", "courses")
            .order_by("-created_on")   # ✅ Latest first
        )

        # ✅ Superuser → all allocations
        if self.request.user.is_superuser:
            return queryset

        # ✅ Normal user → own allocations only
        return queryset.filter(employee=self.request.user)

    def get_context_data(self, **kwargs):

        context = super().get_context_data(**kwargs)

        allocation_data = []

        queryset = context["allocations"]

        # ✅ Counts
        context["approved_count"] = queryset.filter(
            status="APPROVED"
        ).count()

        context["pending_count"] = queryset.filter(
            status="PENDING"
        ).count()

        context["rejected_count"] = queryset.filter(
            status="REJECTED"
        ).count()

        for alloc in queryset:

            course = alloc.courses

            # ✅ Total duration
            total_seconds = (
                course.videos.aggregate(
                    total=Sum("duration")
                )["total"] or 0
            )

            # ✅ Watched duration
            watched_seconds = (
                VideoWatchProgress.objects.filter(
                    employee=alloc.employee,
                    video__course=course
                ).aggregate(
                    total=Sum("watched_duration")
                )["total"] or 0
            )

            # ✅ Progress %
            progress_percent = (
                round((watched_seconds / total_seconds) * 100, 2)
                if total_seconds > 0 else 0
            )

            allocation_data.append({
                "allocation": alloc,
                "course": course,
                "total_hours": round(total_seconds / 3600, 2),
                "watched_hours": round(watched_seconds / 3600, 2),
                "progress_percent": progress_percent,
            })

        context["allocation_data"] = allocation_data
        context["title"] = "Course Allocations"

        return context




# # ---------------- DEALLOCATE COURSES ----------------

# @login_required
# def deallocate_course(request, pk):
#     allocation = get_object_or_404(CourseAllocation, pk=pk)
#     employee = allocation.employee
#     courses = allocation.courses.all()

#     # =============================
#     # 🔔 1. IN-APP NOTIFICATION (TO EMPLOYEE)
#     # =============================
#     for course in courses:
#         Notification.objects.create(
#             sender=request.user,
#             receiver=employee,
#             message=f"You have been removed from the course: {course.title}"
#         )

#     # =============================
#     # 📧 2. EMAIL TO EMPLOYEE
#     # =============================
#     if employee.email:
#         html_message = render_to_string(
#             "emails/course_removed.html",
#             {
#                 "user": employee,
#                 "courses": courses,
#                 "removed_by": request.user,
#                 "now": timezone.now(),
#             }
#         )

#         send_mail_notification(
#             to_emails=[employee.email],
#             subject="Course Deallocated",
#             body="Your assigned course(s) have been removed.",
#             html_message=html_message,
#             request=request
#         )

#     # =============================
#     # 📧 3. EMAIL TO ADMINS
#     # =============================
#     notification_record = SendEmailToReceiveUsers.objects.first()

#     if notification_record:
#         admin_users = notification_record.users.filter(email__isnull=False)
#     else:
#         User = get_user_model()
#         admin_users = User.objects.filter(is_superuser=True, email__isnull=False)

#     for admin in admin_users:
#         send_mail_notification(
#             to_emails=[admin.email],
#             subject="Course Deallocation",
#             body=f"{employee.get_full_name} has been deallocated from courses.",
#             request=request
#         )

#     # =============================
#     # ❌ DELETE ALLOCATION
#     # =============================
#     allocation.delete()

#     # =============================
#     # ✅ SUCCESS MESSAGE
#     # =============================
#     messages.success(request, "Courses successfully deallocated.")

#     return redirect("course_allocation_view")