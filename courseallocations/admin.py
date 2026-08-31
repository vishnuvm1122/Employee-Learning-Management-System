# admin.py

from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.template.loader import render_to_string
from django.urls import path, reverse
from django.utils import timezone
from django.utils.html import format_html
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import (
    ForeignKeyWidget,
    ManyToManyWidget,
)
from .models import (
    Course,
    CourseAllocation,
    PendingCourseAllocation,
)
from notifications.models import Notification
from emailsettings.utils import send_mail_notification


from import_export.widgets import (
    ForeignKeyWidget,
    ManyToManyWidget,
)
from django.contrib.admin.widgets import FilteredSelectMultiple
from django import forms
from course.models import Course

User = get_user_model()





# ==========================================================
# FORM
# ==========================================================
class CourseAllocationForm(forms.ModelForm):

    employees = forms.ModelMultipleChoiceField(
        queryset=User.objects.filter(is_active=True),
        widget=FilteredSelectMultiple(
            "Employees",
            is_stacked=False
        ),
        required=True
    )

    course_list = forms.ModelMultipleChoiceField(
        queryset=Course.objects.all(),
        widget=FilteredSelectMultiple(
            "Courses",
            is_stacked=False
        ),
        required=True
    )

    class Meta:
        model = CourseAllocation

        fields = (
            "employees",
            "course_list",
            "status",
        )

    class Media:

        css = {
            "all": ("admin/css/widgets.css",)
        }

        js = (
            "admin/js/core.js",
            "admin/js/SelectBox.js",
            "admin/js/SelectFilter2.js",
        )


# ==========================================================
# ADMIN
# ==========================================================
@admin.register(CourseAllocation)
class CourseAllocationAdmin(ImportExportModelAdmin):

    form = CourseAllocationForm

    list_display = (
        "employee_name",
        "course_name",
        "status_badge",
        "approved_by",
        "approved_on",
    )

    search_fields = (
        "employee__username",
        "courses__title",
    )

    list_filter = (
        "status",
    )

    ordering = (
        "-id",
    )

    # Hide fields from admin form
    exclude = (
        "employee",
        "courses",
        "approved_by",
        "approved_on",
        "status",
    )

    # ======================================================
    # DISPLAY METHODS
    # ======================================================
    def employee_name(self, obj):

        if obj.employee:

            full_name = (
                f"{obj.employee.first_name} "
                f"{obj.employee.last_name}"
            ).strip()

            # Show: username (Full Name)
            if full_name:
                return f"{obj.employee.username} ({full_name})"

            return obj.employee.username

        return "-"

    employee_name.short_description = "Employee"

    def course_name(self, obj):
        return obj.courses.title if obj.courses else "-"

    course_name.short_description = "Course"

    # ======================================================
    # STATUS BADGE
    # ======================================================
    def status_badge(self, obj):

        colors = {
            "PENDING": "#f39c12",
            "APPROVED": "#27ae60",
            "REJECTED": "#e74c3c",
        }

        return format_html(
            """
            <span style="
                background:{};
                color:white;
                padding:5px 10px;
                border-radius:6px;
                font-size:12px;
                font-weight:600;
            ">
                {}
            </span>
            """,
            colors.get(obj.status, "#777"),
            obj.status
        )

    status_badge.short_description = "Status"

    # ======================================================
    # PREVENT DEFAULT SAVE
    # ======================================================
    def save_model(self, request, obj, form, change):
        pass

    # ======================================================
    # SAVE MULTIPLE USERS + COURSES
    # ======================================================
    def save_related(self, request, form, formsets, change):

        employees = form.cleaned_data.get("employees")
        courses = form.cleaned_data.get("course_list")

        # AUTO STATUS
        status = "APPROVED"

        total = 0
        skipped = 0

        for employee in employees:

            for course in courses:

                # ==========================================
                # CHECK EXISTING
                # ==========================================
                allocation = CourseAllocation.objects.filter(
                    employee=employee,
                    courses=course
                ).first()

                # ==========================================
                # SKIP IF ALREADY APPROVED
                # ==========================================
                if allocation and allocation.status == "APPROVED":

                    skipped += 1

                    self.message_user(
                        request,
                        f"{employee.username} already approved "
                        f"for {course.title}",
                        messages.WARNING
                    )

                    continue

                # ==========================================
                # CREATE NEW
                # ==========================================
                if not allocation:

                    allocation = CourseAllocation(
                        employee=employee,
                        courses=course,
                    )

                # ==========================================
                # AUTO APPROVE
                # ==========================================
                allocation.status = "APPROVED"
                allocation.approved_by = request.user
                allocation.approved_on = timezone.now()

                allocation.save()

                # ==========================================
                # NOTIFICATION
                # ==========================================
                Notification.objects.create(
                    sender=request.user,
                    receiver=employee,
                    message=(
                        f"You have been assigned "
                        f"to course: {course.title}"
                    )
                )

                # ==========================================
                # EMAIL
                # ==========================================
                if employee.email:

                    html_message = render_to_string(
                        "emails/course_updated.html",
                        {
                            "user": employee,
                            "course": course,
                            "status": "APPROVED",
                            "approved_by": request.user,
                            "approved_on": timezone.now(),
                            "now": timezone.now(),
                        }
                    )

                    send_mail_notification(
                        to_emails=[employee.email],
                        subject="Course Allocation",
                        body=(
                            f"You have been assigned "
                            f"to course: {course.title}"
                        ),
                        html_message=html_message
                    )

                total += 1

        # ======================================================
        # SUCCESS MESSAGE
        # ======================================================
        if total > 0:

            self.message_user(
                request,
                f"{total} course allocations created successfully.",
                messages.SUCCESS
            )

        # ======================================================
        # SKIPPED MESSAGE
        # ======================================================
        if skipped > 0:

            self.message_user(
                request,
                f"{skipped} already approved allocations skipped.",
                messages.WARNING
            )



# ==========================================================
# PENDING COURSE RESOURCE
# ==========================================================
class PendingCourseAllocationResource(
    resources.ModelResource
):

    employee = fields.Field(
        column_name="employee",
        attribute="employee",
        widget=ForeignKeyWidget(
            User,
            "username"
        )
    )

    courses = fields.Field(
        column_name="courses",
        attribute="courses",
        widget=ManyToManyWidget(
            Course,
            field="title",
            separator=","
        )
    )

    class Meta:
        model = PendingCourseAllocation


# ==========================================================
# PENDING COURSE ADMIN
# ==========================================================
@admin.register(PendingCourseAllocation)
class PendingCourseAllocationAdmin(
    ImportExportModelAdmin
):

    def has_add_permission(self, request):
        return False

    # =====================================================
    # CONFIGURATION
    # =====================================================

    resource_class = (
        PendingCourseAllocationResource
    )

    list_display = (
        "employee_name",
        "course_name",
        "requested_date",
        "approved_date",
        "status_badge",
        "approve_button",
        "reject_button",
    )

    search_fields = (
        "employee__username",
        "courses__title",
    )

    list_filter = (
        "status",
        "created_on",
        "approved_on",
    )

    ordering = (
        "-id",
    )

    readonly_fields = (
        "approved_by",
        "approved_on",
        "created_on",
    )

    list_per_page = 20

    # =====================================================
    # EMPLOYEE NAME
    # =====================================================

    def employee_name(self, obj):

        if obj.employee:

            full_name = (
                f"{obj.employee.first_name} "
                f"{obj.employee.last_name}"
            ).strip()

            # Show: username (Full Name)
            if full_name:
                return f"{obj.employee.username} ({full_name})"

            return obj.employee.username

        return "-"

    employee_name.short_description = "Employee"

    # =====================================================
    # COURSE NAME
    # =====================================================

    def course_name(self, obj):

        if obj.courses:
            return obj.courses.title

        return "-"

    course_name.short_description = "Course"

    # =====================================================
    # REQUESTED DATE
    # =====================================================

    def requested_date(self, obj):

        if obj.created_on:

            return obj.created_on.strftime(
                "%d %b %Y | %I:%M %p"
            )

        return "-"

    requested_date.short_description = (
        "Requested On"
    )

    # =====================================================
    # APPROVED DATE
    # =====================================================

    def approved_date(self, obj):

        if obj.approved_on:

            return obj.approved_on.strftime(
                "%d %b %Y | %I:%M %p"
            )

        return "-"

    approved_date.short_description = (
        "Approved On"
    )

    # =====================================================
    # STATUS BADGE
    # =====================================================

    def status_badge(self, obj):

        colors = {
            "PENDING": "#f39c12",
            "APPROVED": "#27ae60",
            "REJECTED": "#e74c3c",
        }

        icons = {
            "PENDING": "⏳",
            "APPROVED": "✅",
            "REJECTED": "❌",
        }

        return format_html(
            """
            <span style="
                background:{};
                color:white;
                padding:6px 14px;
                border-radius:30px;
                font-size:12px;
                font-weight:700;
                letter-spacing:.5px;
            ">
                {} {}
            </span>
            """,
            colors.get(obj.status, "#777"),
            icons.get(obj.status, ""),
            obj.status
        )

    status_badge.short_description = "Status"

    # =====================================================
    # APPROVE BUTTON
    # =====================================================

    def approve_button(self, obj):

        if obj.status == "PENDING":

            url = reverse(
                "admin:pendingcourseallocation_approve",
                args=[obj.pk]
            )

            return format_html(
                """
                <a href="{}"
                   style="
                        background:#27ae60;
                        color:white;
                        padding:7px 14px;
                        border-radius:6px;
                        text-decoration:none;
                        font-weight:600;
                        display:inline-block;
                   ">
                    ✔ Approve
                </a>
                """,
                url
            )

        return "-"

    approve_button.short_description = "Approve"

    # =====================================================
    # REJECT BUTTON
    # =====================================================

    def reject_button(self, obj):

        if obj.status == "PENDING":

            url = reverse(
                "admin:pendingcourseallocation_reject",
                args=[obj.pk]
            )

            return format_html(
                """
                <a href="{}"
                   style="
                        background:#e74c3c;
                        color:white;
                        padding:7px 14px;
                        border-radius:6px;
                        text-decoration:none;
                        font-weight:600;
                        display:inline-block;
                   ">
                    ✖ Reject
                </a>
                """,
                url
            )

        return "-"

    reject_button.short_description = "Reject"

    # =====================================================
    # CUSTOM ADMIN URLS
    # =====================================================

    def get_urls(self):

        urls = super().get_urls()

        custom_urls = [

            path(
                "approve/<int:pk>/",
                self.admin_site.admin_view(
                    self.approve_request
                ),
                name="pendingcourseallocation_approve",
            ),

            path(
                "reject/<int:pk>/",
                self.admin_site.admin_view(
                    self.reject_request
                ),
                name="pendingcourseallocation_reject",
            ),

        ]

        return custom_urls + urls

    # =====================================================
    # SAVE MODEL
    # =====================================================

    def save_model(
        self,
        request,
        obj,
        form,
        change
    ):

        old_status = None

        if change:

            old_obj = (
                PendingCourseAllocation.objects.get(
                    pk=obj.pk
                )
            )

            old_status = old_obj.status

        super().save_model(
            request,
            obj,
            form,
            change
        )

        if (
            change and
            old_status != obj.status
        ):

            if obj.status == "APPROVED":

                obj.approved_by = request.user
                obj.approved_on = timezone.now()

                obj.save()

            self.send_notification(
                request,
                obj
            )

    # =====================================================
    # UPDATE STATUS
    # =====================================================

    def update_status(
        self,
        request,
        pk,
        status
    ):

        obj = (
            PendingCourseAllocation.objects.get(
                pk=pk
            )
        )

        obj.status = status
        obj.approved_by = request.user

        if status == "APPROVED":

            obj.approved_on = timezone.now()

        obj.save()

        # ============================================
        # SEND NOTIFICATIONS
        # ============================================

        self.send_notification(
            request,
            obj
        )

        # ============================================
        # SUCCESS MESSAGE
        # ============================================

        self.message_user(
            request,
            f"{obj.courses.title} "
            f"{status.title()} Successfully",
            messages.SUCCESS
        )

        # ============================================
        # REDIRECT TO CURRENT ADMIN PAGE
        # ============================================

        return HttpResponseRedirect(
            reverse(
                "admin:courseallocations_pendingcourseallocation_changelist"
            )
        )

    # =====================================================
    # APPROVE REQUEST
    # =====================================================

    def approve_request(
        self,
        request,
        pk
    ):

        return self.update_status(
            request,
            pk,
            "APPROVED"
        )

    # =====================================================
    # REJECT REQUEST
    # =====================================================

    def reject_request(
        self,
        request,
        pk
    ):

        return self.update_status(
            request,
            pk,
            "REJECTED"
        )

    # =====================================================
    # SEND NOTIFICATION
    # =====================================================

    def send_notification(
        self,
        request,
        obj
    ):

        # ============================================
        # DATABASE NOTIFICATION
        # ============================================

        Notification.objects.create(
            sender=request.user,
            receiver=obj.employee,
            message=(
                f"Your request for "
                f"{obj.courses.title} "
                f"has been "
                f"{obj.status.lower()}."
            )
        )

        # ============================================
        # EMAIL NOTIFICATION
        # ============================================

        if (
            obj.employee and
            obj.employee.email
        ):

            try:

                html_message = render_to_string(
                    "emails/course_status.html",
                    {
                        "user": obj.employee,
                        "status": obj.status,
                        "course": obj.courses,
                        "approved_by": request.user,
                        "approved_on": obj.approved_on,
                        "requested_on": obj.created_on,
                        "now": timezone.now(),
                    }
                )

                send_mail_notification(
                    to_emails=[
                        obj.employee.email
                    ],

                    subject=(
                        f"Course Request "
                        f"{obj.status.title()}"
                    ),

                    body=(
                        f"Your request for "
                        f"{obj.courses.title} "
                        f"has been "
                        f"{obj.status.lower()}."
                    ),

                    html_message=html_message
                )

            except Exception as e:

                self.message_user(
                    request,
                    f"Email sending failed: {str(e)}",
                    level=messages.WARNING
                )