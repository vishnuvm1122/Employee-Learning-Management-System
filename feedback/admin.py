from django.contrib import admin
from django.contrib import messages
from django.template.loader import render_to_string
from django.utils import timezone
from django.utils.html import format_html

from emailsettings.utils import send_mail_notification
from notifications.models import Notification

from .models import Feedback


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):

    list_display = (
        "id",
        "user",
        "course",
        "rating",
        "stars_display",
        "reply_status",
        "created_at",
    )

    readonly_fields = (
        "created_at",
        "updated_at",
        "replied_at",
    )

    search_fields = (
        "user__username",
        "course__title",
        "comment",
    )

    list_filter = (
        "rating",
        "created_at",
    )

    ordering = (
        "-created_at",
    )

    fieldsets = (

        (
            "Feedback",
            {
                "fields": (
                    "user",
                    "course",
                    "rating",
                    "comment",
                )
            },
        ),

        (
            "Reply",
            {
                "fields": (
                    "reply",
                    "replied_by",
                    "replied_at",
                )
            },
        ),

        (
            "Dates",
            {
                "fields": (
                    "created_at",
                    "updated_at",
                )
            },
        ),
    )

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

        if obj.reply:

            obj.replied_by = request.user

            if not obj.replied_at:

                obj.replied_at = timezone.now()

        super().save_model(
            request,
            obj,
            form,
            change
        )

        # =================================================
        # NOTIFICATION
        # =================================================

        try:

            Notification.objects.create(
                sender=request.user,
                receiver=obj.user,
                title="Feedback Replied",
                message=(
                    f"Your feedback for "
                    f"{obj.course.title} "
                    f"has been replied."
                )
            )

        except Exception as e:

            print(e)

        # =================================================
        # EMAIL
        # =================================================

        if obj.user.email:

            try:

                html_message = render_to_string(
                    "emails/feedback_replied.html",
                    {
                        "user": obj.user,
                        "feedback": obj,
                        "reply": obj.reply,
                        "replier": request.user,
                    }
                )

                send_mail_notification(

                    to_emails=[
                        obj.user.email
                    ],

                    subject="Feedback Replied",

                    body=(
                        f"Your feedback has "
                        f"been replied."
                    ),

                    html_message=html_message,

                    request=request,
                )

            except Exception as e:

                self.message_user(
                    request,
                    str(e),
                    level=messages.ERROR,
                )

    # =====================================================
    # STARS
    # =====================================================

    def stars_display(self, obj):

        try:

            return format_html(
                '<span style="color:orange;">{}</span>',
                "★" * obj.rating
            )

        except Exception:

            return "-"

    stars_display.short_description = "Stars"

    # =====================================================
    # STATUS
    # =====================================================

    def reply_status(self, obj):

        try:

            if obj.reply:

                return format_html(
                    '<span style="color:green;">✔ Replied</span>'
                )

            return format_html(
                '<span style="color:red;">✘ Pending</span>'
            )

        except Exception:

            return "-"

    reply_status.short_description = "Status"