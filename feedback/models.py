from django.conf import settings
from django.db import models
from django.utils import timezone

from course.models import Course


# =========================================================
# FEEDBACK MODEL
# =========================================================
class Feedback(models.Model):

    # =====================================================
    # USER
    # =====================================================
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    # =====================================================
    # COURSE
    # =====================================================
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="feedbacks",
    )

    # =====================================================
    # RATING
    # =====================================================
    rating = models.PositiveSmallIntegerField(
        default=5
    )

    # =====================================================
    # COMMENT
    # =====================================================
    comment = models.TextField(
        blank=True
    )

    # =====================================================
    # ADMIN REPLY
    # =====================================================
    reply = models.TextField(
        blank=True,
        null=True
    )

    # =====================================================
    # REPLIED USER
    # =====================================================
    replied_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="feedback_replies",
    )

    # =====================================================
    # REPLIED DATE
    # =====================================================
    replied_at = models.DateTimeField(
        null=True,
        blank=True
    )

    # =====================================================
    # CREATED DATE
    # =====================================================
    created_at = models.DateTimeField(
        auto_now_add=True
    )

    # =====================================================
    # UPDATED DATE
    # =====================================================
    updated_at = models.DateTimeField(
        auto_now=True
    )

    # =====================================================
    # META
    # =====================================================
    class Meta:

        verbose_name = "Feedback"
        verbose_name_plural = "Feedbacks"

        ordering = [
            "-created_at"
        ]

        unique_together = (
            "user",
            "course",
        )

    # =====================================================
    # STRING REPRESENTATION
    # =====================================================
    def __str__(self):

        return (
            f"{self.user} - "
            f"{self.course} "
            f"({self.rating}/5)"
        )

    # =====================================================
    # STAR DISPLAY
    # =====================================================
    def stars(self):

        return "⭐" * int(self.rating)

    # =====================================================
    # CHECK REPLIED
    # =====================================================
    @property
    def is_replied(self):

        return bool(self.reply)

    # =====================================================
    # SAVE
    # =====================================================
    def save(self, *args, **kwargs):

        # Auto set replied time
        if self.reply and not self.replied_at:

            self.replied_at = timezone.now()

        super().save(*args, **kwargs)