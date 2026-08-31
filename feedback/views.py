from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.shortcuts import (
    get_object_or_404,
    redirect,
    render,
)
from django.template.loader import render_to_string
from django.urls import reverse
from django.utils import timezone
from django.views.decorators.http import require_POST

from accounts.decorators import admin_required
from courseallocations.models import CourseAllocation
from emailsettings.utils import send_mail_notification
from notifications.models import Notification

from .forms import FeedbackForm
from .models import Feedback

User = get_user_model()


# =========================================================
# ADD FEEDBACK
# =========================================================
@login_required
def add_feedback(request):

    # =====================================================
    # GET ALLOCATED COURSES
    # =====================================================
    allocations = CourseAllocation.objects.filter(
        employee=request.user
    ).select_related("courses")

    assigned_courses = [
        alloc.courses
        for alloc in allocations
        if alloc.courses
    ]

    # =====================================================
    # REMOVE DUPLICATES
    # =====================================================
    assigned_courses = list(
        {
            course.id: course
            for course in assigned_courses
        }.values()
    )

    # =====================================================
    # NO COURSES
    # =====================================================
    if not assigned_courses:

        messages.warning(
            request,
            "⚠ You have no allocated courses."
        )

        return redirect("dashboard")

    # =====================================================
    # DEFAULT VALUES
    # =====================================================
    selected_course = assigned_courses[0]

    existing_feedback = Feedback.objects.filter(
        user=request.user,
        course=selected_course
    ).first()

    form = FeedbackForm(
        instance=existing_feedback
    )

    # =====================================================
    # POST
    # =====================================================
    if request.method == "POST":

        course_id = request.POST.get("course")

        # =================================================
        # FIND SELECTED COURSE
        # =================================================
        selected_course = next(
            (
                c for c in assigned_courses
                if str(c.id) == str(course_id)
            ),
            None
        )

        if not selected_course:

            messages.error(
                request,
                "⚠ Invalid course selected."
            )

            return redirect("add_feedback")

        # =================================================
        # EXISTING FEEDBACK
        # =================================================
        existing_feedback = Feedback.objects.filter(
            user=request.user,
            course=selected_course
        ).first()

        # =================================================
        # FORM
        # =================================================
        form = FeedbackForm(
            request.POST,
            instance=existing_feedback
        )

        # =================================================
        # VALIDATION
        # =================================================
        if form.is_valid():

            feedback = form.save(commit=False)

            feedback.user = request.user
            feedback.course = selected_course

            feedback.save()

            # =============================================
            # SUCCESS MESSAGE
            # =============================================
            if existing_feedback:

                messages.success(
                    request,
                    "✅ Feedback updated successfully."
                )

            else:

                messages.success(
                    request,
                    "✅ Feedback submitted successfully."
                )

            # =============================================
            # ADMINS
            # =============================================
            admins = User.objects.filter(
                is_superuser=True
            ).exclude(
                email__isnull=True
            ).exclude(
                email=""
            )

            # =============================================
            # SEND NOTIFICATION + EMAIL
            # =============================================
            for admin in admins:

                # -----------------------------------------
                # NOTIFICATION
                # -----------------------------------------
                try:

                    Notification.objects.create(
                        sender=request.user,
                        receiver=admin,
                        message=(
                            f"{request.user.username} "
                            f"submitted feedback for "
                            f"{selected_course.title}."
                        )
                    )

                except Exception as e:

                    print("Notification Error:", e)

                # -----------------------------------------
                # EMAIL
                # -----------------------------------------
                try:

                    html_message = render_to_string(
                        "emails/feedback_submitted.html",
                        {
                            "user": admin,
                            "feedback_user": request.user,
                            "course": selected_course,
                            "feedback": feedback,
                            "login_link": request.build_absolute_uri(
                                reverse("dashboard")
                            ),
                        }
                    )

                    send_mail_notification(
                        to_emails=[admin.email],
                        subject="New Feedback Submitted",
                        body=(
                            f"{request.user.username} "
                            f"submitted feedback for "
                            f"{selected_course.title}.\n\n"
                            f"Rating: {feedback.rating}\n"
                            f"Comment: {feedback.comment}"
                        ),
                        html_message=html_message,
                        request=request,
                    )

                except Exception as e:

                    print("Email Error:", e)

            # =============================================
            # IMPORTANT REDIRECT
            # =============================================
            return redirect("feedback_list")

        # =================================================
        # INVALID FORM
        # =================================================
        else:

            print(form.errors)

            messages.error(
                request,
                "⚠ Please correct the form errors."
            )

    # =====================================================
    # RENDER
    # =====================================================
    return render(
        request,
        "feedback/feedback_form.html",
        {
            "form": form,
            "assigned_courses": assigned_courses,
            "selected_course": selected_course,
        }
    )


# =========================================================
# EDIT FEEDBACK
# =========================================================
@login_required
def edit_feedback(request, pk):

    feedback = get_object_or_404(
        Feedback.objects.select_related(
            "user",
            "course"
        ),
        pk=pk
    )

    # =====================================================
    # PERMISSION CHECK
    # =====================================================
    if feedback.user != request.user:

        messages.error(
            request,
            "⚠ Permission denied."
        )

        return redirect("feedback_list")

    # =====================================================
    # POST
    # =====================================================
    if request.method == "POST":

        form = FeedbackForm(
            request.POST,
            instance=feedback
        )

        if form.is_valid():

            updated_feedback = form.save(commit=False)

            updated_feedback.user = request.user
            updated_feedback.course = feedback.course

            updated_feedback.save()

            messages.success(
                request,
                "✅ Feedback updated successfully."
            )

            # =============================================
            # ADMINS
            # =============================================
            admins = User.objects.filter(
                is_superuser=True
            ).exclude(
                email__isnull=True
            ).exclude(
                email=""
            )

            for admin in admins:

                # -----------------------------------------
                # NOTIFICATION
                # -----------------------------------------
                try:

                    Notification.objects.create(
                        sender=request.user,
                        receiver=admin,
                        message=(
                            f"{request.user.username} "
                            f"updated feedback for "
                            f"{feedback.course.title}."
                        )
                    )

                except Exception as e:

                    print("Notification Error:", e)

                # -----------------------------------------
                # EMAIL
                # -----------------------------------------
                try:

                    html_message = render_to_string(
                        "emails/feedback_updated.html",
                        {
                            "user": admin,
                            "feedback_user": request.user,
                            "course": feedback.course,
                            "feedback": updated_feedback,
                        }
                    )

                    send_mail_notification(
                        to_emails=[admin.email],
                        subject="Feedback Updated",
                        body=(
                            f"{request.user.username} "
                            f"updated feedback for "
                            f"{feedback.course.title}."
                        ),
                        html_message=html_message,
                        request=request,
                    )

                except Exception as e:

                    print("Email Error:", e)

            return redirect("feedback_list")

        else:

            print(form.errors)

            messages.error(
                request,
                "⚠ Please correct form errors."
            )

    else:

        form = FeedbackForm(
            instance=feedback
        )

    # =====================================================
    # RENDER
    # =====================================================
    return render(
        request,
        "feedback/feedback_form.html",
        {
            "form": form,
            "feedback": feedback,
            "selected_course": feedback.course,
            "assigned_courses": [feedback.course],
            "is_edit": True,
        }
    )


# =========================================================
# DELETE FEEDBACK
# =========================================================
@login_required
@require_POST
def delete_feedback(request, pk):

    # =====================================================
    # GET FEEDBACK
    # =====================================================
    feedback = get_object_or_404(
        Feedback.objects.select_related(
            "user",
            "course"
        ),
        pk=pk
    )

    # =====================================================
    # PERMISSION CHECK
    # =====================================================
    if feedback.user != request.user:

        return JsonResponse(
            {
                "success": False,
                "message": "Permission denied."
            },
            status=403
        )

    # =====================================================
    # STORE VALUES BEFORE DELETE
    # =====================================================
    course_title = feedback.course.title
    feedback_user = feedback.user

    # =====================================================
    # DELETE FEEDBACK
    # =====================================================
    feedback.delete()

    # =====================================================
    # SUCCESS MESSAGE
    # =====================================================
    messages.success(
        request,
        "✅ Feedback deleted successfully."
    )

    # =====================================================
    # GET ADMINS
    # =====================================================
    admins = User.objects.filter(
        is_superuser=True
    ).exclude(
        email__isnull=True
    ).exclude(
        email=""
    )

    # =====================================================
    # SEND NOTIFICATION + EMAIL
    # =====================================================
    for admin in admins:

        # -------------------------------------------------
        # NORMAL NOTIFICATION
        # -------------------------------------------------
        try:

            Notification.objects.create(
                sender=request.user,
                receiver=admin,
                message=(
                    f"{request.user.username} "
                    f"deleted feedback for "
                    f"{course_title}."
                )
            )

        except Exception as e:

            print("Notification Error:", e)

        # -------------------------------------------------
        # EMAIL NOTIFICATION
        # -------------------------------------------------
        try:

            html_message = render_to_string(
                "emails/feedback_deleted.html",
                {
                    "user": admin,
                    "feedback_user": feedback_user,
                    "course_title": course_title,
                    "login_link": request.build_absolute_uri(
                        reverse("dashboard")
                    ),
                }
            )

            send_mail_notification(
                to_emails=[admin.email],
                subject="Feedback Deleted",
                body=(
                    f"{request.user.username} "
                    f"deleted feedback for "
                    f"{course_title}."
                ),
                html_message=html_message,
                request=request,
            )

        except Exception as e:

            print("Email Error:", e)

    # =====================================================
    # JSON RESPONSE
    # =====================================================
    return JsonResponse(
        {
            "success": True,
            "message": "Feedback deleted successfully.",
            "redirect_url": reverse(
                "feedback_list"
            )
        }
    )


# =========================================================
# REPLY FEEDBACK
# =========================================================
@login_required
@admin_required
def reply_feedback(request, pk):

    feedback = get_object_or_404(
        Feedback.objects.select_related(
            "user",
            "course"
        ),
        pk=pk
    )

    # =====================================================
    # POST
    # =====================================================
    if request.method == "POST":

        reply_text = request.POST.get(
            "reply",
            ""
        ).strip()

        # =================================================
        # EMPTY CHECK
        # =================================================
        if not reply_text:

            messages.error(
                request,
                "⚠ Reply cannot be empty."
            )

            return redirect(
                "reply_feedback",
                pk=feedback.pk
            )

        # =================================================
        # SAVE REPLY
        # =================================================
        feedback.reply = reply_text
        feedback.replied_by = request.user
        feedback.replied_at = timezone.now()

        feedback.save()

        # =================================================
        # SUCCESS MESSAGE
        # =================================================
        messages.success(
            request,
            "✅ Reply submitted successfully."
        )

        # =================================================
        # USER NOTIFICATION
        # =================================================
        try:

            Notification.objects.create(
                sender=request.user,
                receiver=feedback.user,
                message=(
                    f"Your feedback for "
                    f"{feedback.course.title} "
                    f"has been replied."
                )
            )

        except Exception as e:

            print("Notification Error:", e)

        # =================================================
        # EMAIL
        # =================================================
        if feedback.user.email:

            try:

                html_message = render_to_string(
                    "emails/feedback_replied.html",
                    {
                        "user": feedback.user,
                        "feedback": feedback,
                        "reply": reply_text,
                        "replier": request.user,
                    }
                )

                send_mail_notification(
                    to_emails=[
                        feedback.user.email
                    ],
                    subject="Feedback Replied",
                    body=(
                        f"Your feedback for "
                        f"{feedback.course.title} "
                        f"has been replied.\n\n"
                        f"Reply:\n{reply_text}"
                    ),
                    html_message=html_message,
                    request=request,
                )

            except Exception as e:

                print("Email Error:", e)

        return redirect("feedback_list")

    # =====================================================
    # GET
    # =====================================================
    return render(
        request,
        "feedback/reply_form.html",
        {
            "feedback": feedback
        }
    )


# =========================================================
# FEEDBACK LIST
# =========================================================
@login_required
def feedback_list(request):

    feedbacks = Feedback.objects.select_related(
        "user",
        "course",
        "replied_by"
    )

    # =====================================================
    # NORMAL USER
    # =====================================================
    if not request.user.is_superuser:

        feedbacks = feedbacks.filter(
            user=request.user
        )

    feedbacks = feedbacks.order_by(
        "-created_at"
    )

    return render(
        request,
        "feedback/feedback_list.html",
        {
            "feedbacks": feedbacks
        }
    )