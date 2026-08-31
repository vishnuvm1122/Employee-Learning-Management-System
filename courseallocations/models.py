from django.conf import settings
from django.db import models
from django.urls import reverse
from django.utils import timezone

from course.models import Course


# =========================================================
# COURSE ALLOCATION MODEL
# =========================================================
class CourseAllocation(models.Model):

    # =====================================================
    # STATUS CHOICES
    # =====================================================
    STATUS_CHOICES = (
        ("PENDING", "Pending"),
        ("APPROVED", "Approved"),
        ("REJECTED", "Rejected"),
    )

    # =====================================================
    # EMPLOYEE
    # =====================================================
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="course_allocations",
        null=True,
        blank=True
    )

    created_on = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # COURSE
    # =====================================================
    courses = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="allocations"
    )

    # =====================================================
    # APPROVAL DETAILS
    # =====================================================
    approved_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="approved_course_allocations"
    )

    approved_on = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # STATUS
    # =====================================================
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="PENDING"
    )

    # =====================================================
    # REMARKS
    # =====================================================
    remarks = models.TextField(
        blank=True,
        null=True,
        help_text="Enter rejection reason or admin remarks."
    )

    # =====================================================
    # CREATED DATE
    # =====================================================
    created_on = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # META
    # =====================================================
    class Meta:

        verbose_name = "Course Allocation"
        verbose_name_plural = "Course Allocations"
        ordering = ["-id"]

    # =====================================================
    # STRING
    # =====================================================
    def __str__(self):

        if self.employee and self.courses:

            return (
                f"{self.employee.username} "
                f"- "
                f"{self.courses.title}"
            )

        return "Unassigned Allocation"

    # =====================================================
    # ABSOLUTE URL
    # =====================================================
    def get_absolute_url(self):

        return reverse(
            "edit_allocated_course",
            kwargs={"pk": self.pk}
        )

    # =====================================================
    # COURSE LIST
    # =====================================================
    def course_list(self):

        if self.courses:

            return self.courses.title

        return "-"

    course_list.short_description = "Course"

    # =====================================================
    # APPROVE
    # =====================================================
    def approve(self, approved_user):

        self.status = "APPROVED"
        self.approved_by = approved_user
        self.approved_on = timezone.now()
        self.remarks = ""

        self.save()

    # =====================================================
    # REJECT
    # =====================================================
    def reject(self, approved_user, reason=""):

        self.status = "REJECTED"
        self.approved_by = approved_user
        self.approved_on = timezone.now()
        self.remarks = reason

        self.save()


# =========================================================
# PENDING COURSE ALLOCATION
# =========================================================
class PendingCourseAllocation(CourseAllocation):

    class Meta:

        proxy = True
        verbose_name = "Pending Course Allocation"
        verbose_name_plural = "Pending Course Allocations"