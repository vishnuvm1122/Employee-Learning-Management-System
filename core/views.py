from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from accounts.decorators import admin_required
from .forms import NewsAndEventsForm
from .models import NewsAndEvents, ActivityLog
from accounts.models import User
import os
from course.models import* 
from quiz.models import* 
from django.db.models import Count
from django.core.serializers.json import DjangoJSONEncoder
import json

from django.db.models import Count, Q
from django.shortcuts import render
import json

# ========================================================
# News & Events
# ========================================================

@login_required
def home_view(request):
    items = NewsAndEvents.objects.all().order_by("-updated_date")

    return render(request, "core/index.html", {
        "title": "News & Events",
        "items": items,
    })




@admin_required
def dashboard_view(request):
    # -------------------------
    # Users Stats
    # -------------------------
    total_users = User.objects.count()
    males_count = User.objects.filter(gender="M").count()
    females_count = User.objects.filter(gender="F").count()
    active_employees = User.objects.filter(is_active=True).count()
    inactive_employees = User.objects.filter(is_active=False).count()

    # -------------------------
    # Programs & Courses
    # -------------------------
    total_programs = Program.objects.count()
    total_courses = Course.objects.count()

    # -------------------------
    # Quizzes Stats (using Sitting)
    # -------------------------
    total_quizzes = Sitting.objects.count()
    completed_quizzes = Sitting.objects.filter(complete=True).count()
    pending_quizzes = total_quizzes - completed_quizzes

    # -------------------------
    # Latest Activity Logs
    # -------------------------
    logs = ActivityLog.objects.all().order_by('-timestamp')[:10]

    # -------------------------
    # Charts Data
    # -------------------------
    gender_chart_labels = ["Male", "Female"]
    gender_chart_data = [males_count, females_count]

    quiz_chart_labels = ["Completed", "Pending"]
    quiz_chart_data = [completed_quizzes, pending_quizzes]

    # Courses per Program
    programs = Program.objects.annotate(course_count=Count('courses'))
    program_chart_labels = [p.title for p in programs]
    program_chart_data = [p.course_count for p in programs]

    context = {
        "total_users": total_users,
        "active_employees": active_employees,
        "inactive_employees": inactive_employees,
        "total_programs": total_programs,
        "total_courses": total_courses,
        "total_quizzes": total_quizzes,
        "completed_quizzes": completed_quizzes,
        "pending_quizzes": pending_quizzes,
        "logs": logs,
        # Chart data (JSON for JS)
        "gender_chart_labels": json.dumps(gender_chart_labels),
        "gender_chart_data": json.dumps(gender_chart_data),
        "quiz_chart_labels": json.dumps(quiz_chart_labels),
        "quiz_chart_data": json.dumps(quiz_chart_data),
        "program_chart_labels": json.dumps(program_chart_labels),
        "program_chart_data": json.dumps(program_chart_data),
    }

    return render(request, "core/dashboard.html", context)



@admin_required
@login_required
def post_add(request):
    form = NewsAndEventsForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        title = form.cleaned_data.get("title", "Post")
        form.save()
        messages.success(request, f"{title} uploaded successfully.")
        return redirect("home")

    return render(request, "core/post_add.html", {
        "title": "Add Post",
        "form": form,
    })

@admin_required
@login_required
def edit_post(request, pk):
    instance = get_object_or_404(NewsAndEvents, pk=pk)

    form = NewsAndEventsForm(
        request.POST or None,
        request.FILES or None,
        instance=instance
    )

    if form.is_valid():
        post = form.save()  # django-cleanup handles file deletion

        messages.success(
            request,
            f"{post.title or 'Post'} updated successfully."
        )
        return redirect("home")

    return render(request, "core/post_add.html", {
        "title": "Edit Post",
        "form": form,
        "instance": instance,  # optional (useful for preview UI)
    })

@admin_required
@login_required
def delete_post(request, pk):
    post = get_object_or_404(NewsAndEvents, pk=pk)

    title = post.title
    post.delete()  # django-cleanup handles image deletion

    messages.success(request, f"{title or 'Post'} deleted successfully.")
    return redirect("home")


@login_required
def post_detail(request, pk):
    item = get_object_or_404(NewsAndEvents, pk=pk)
    return render(request, "core/post_detail.html", {"item": item})



def custom_404(request, exception):
    return render(request, "errors/404.html", status=404)

def custom_500(request):
    return render(request, "errors/500.html", status=500)

def custom_403(request, exception):
    return render(request, "errors/403.html", status=403)

def custom_400(request, exception):
    return render(request, "errors/400.html", status=400)