from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.core.paginator import Paginator
from django_filters.views import FilterView
from .models import *
from .forms import*
from .filters import ProgramFilter
from django.conf import settings
from django.http import JsonResponse
from django.shortcuts import get_object_or_404
import json 
from courseallocations.models import *
from accounts.decorators import admin_required, staff_required

##email modules
from django.utils import timezone
from emailsettings.models import *
from emailsettings.utils import *
from notifications.models import Notification
from django.contrib.auth import get_user_model
from django.template.loader import render_to_string
from django.db.models import Avg



# ========================
# Program List (Filter View)
# ========================
@method_decorator(login_required, name='dispatch')
class ProgramFilterView(FilterView):
    model = Program
    filterset_class = ProgramFilter
    template_name = "course/program_list.html"
    paginate_by = 10

    def get_queryset(self):
        return Program.objects.all().order_by("-id")

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # TITLE
        context["title"] = "Programs"

        # PAGINATION OBJECTS
        context["page_obj"] = context.get("page_obj")
        context["paginator"] = context.get("paginator")
        context["is_paginated"] = context.get("is_paginated")

        return context

# ========================
# Add Program
# ========================
@login_required
@admin_required
def program_add(request):
    form = ProgramForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        program = form.save()
        messages.success(request, f"{program.title} program has been created.")
        return redirect("programs")

    return render(request, "course/program_add.html", {
        "title": "Add Program",
        "form": form
    })


# ========================
# Edit Program
# ========================
@login_required
@admin_required
def program_edit(request, pk):
    program = get_object_or_404(Program, pk=pk)

    form = ProgramForm(
        request.POST or None,
        request.FILES or None,
        instance=program
    )

    if form.is_valid():
        program = form.save()  # django-cleanup will handle image replacement
        messages.success(request, f"{program.title} updated successfully.")
        return redirect("programs")

    return render(request, "course/program_add.html", {
        "title": "Edit Program",
        "form": form,
        "instance": program  # for preview
    })


# ========================
# Delete Program
# ========================
@login_required
@admin_required
def program_delete(request, pk):
    program = get_object_or_404(Program, pk=pk)

    if request.method == "POST":
        title = program.title
        program.delete()  # django-cleanup handles file deletion

        messages.success(request, f"Program '{title}' deleted successfully.")
        return redirect("programs")

    return redirect("programs")  # no template (as per your style)


# ========================
# Program Detail
# ========================

# views.py




@login_required
@login_required
def program_detail(request, pk):

    # =========================================
    # PROGRAM
    # =========================================
    program = get_object_or_404(
        Program,
        pk=pk
    )

    # =========================================
    # COURSES
    # =========================================
    courses_qs = (
        Course.objects.filter(program=program)
        .prefetch_related("videos")
        .order_by("title")
    )

    # =========================================
    # ALLOCATED COURSES
    # =========================================
    allocated_courses = []
    allocated_course_ids = []

    if not request.user.is_superuser:

        allocations = (
            CourseAllocation.objects.filter(
                employee=request.user
            )
            .select_related("courses")
        )

        for allocation in allocations:

            allocated_courses.append({
                "course_id": allocation.courses.id,
                "course_title": allocation.courses.title,
                "status": allocation.status,
                "approved_on": allocation.approved_on,
                "created_on": allocation.created_on,
            })

            allocated_course_ids.append(
                allocation.courses.id
            )

    # =========================================
    # COURSE PROGRESS
    # =========================================
    for course in courses_qs:

        # Total watched duration
        watched_duration = (
            VideoWatchProgress.objects.filter(
                video__course=course,
                employee=request.user
            ).aggregate(
                total=Avg("watched_duration")
            )
        )

        watched = watched_duration["total"] or 0

        # Total course video duration
        total_duration = sum(
            video.duration or 0
            for video in course.videos.all()
        )

        # Progress calculation
        if total_duration > 0:

            course.progress = round(
                (watched / total_duration) * 100,
                2
            )

            if course.progress > 100:
                course.progress = 100

        else:
            course.progress = 0

    # =========================================
    # PAGINATION
    # =========================================
    paginator = Paginator(
        courses_qs,
        9
    )

    page_number = request.GET.get("page")

    courses = paginator.get_page(
        page_number
    )

    # =========================================
    # CONTEXT
    # =========================================
    context = {
        "title": program.title,
        "program": program,
        "courses": courses,
        "allocated_courses": allocated_courses,
        "allocated_course_ids": allocated_course_ids,
    }

    # =========================================
    # RENDER
    # =========================================
    return render(
        request,
        "course/course_list.html",
        context
    )
    
# ========================
# ADD COURSE
# ========================
@login_required
@admin_required
def course_add(request, pk):
    program = get_object_or_404(Program, pk=pk)

    form = CourseAddForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        course = form.save(commit=False)
        course.program = program  # assign FK
        course.save()

        messages.success(
            request, f"{course.title} ({course.code}) created successfully."
        )
        return redirect("program_detail", pk=program.pk)

    return render(request, "course/course_add.html", {
        "title": "Add Course",
        "form": form,
        "program": program
    })


# ========================
# EDIT COURSE
# ========================
@login_required
@admin_required
def course_edit(request, pk):
    course = get_object_or_404(Course, id=pk)

    form = CourseAddForm(
        request.POST or None,
        request.FILES or None,
        instance=course
    )

    if form.is_valid():
        course = form.save()  # django-cleanup handles old image
        messages.success(
            request, f"{course.title} ({course.code}) updated successfully."
        )
        return redirect("program_detail", pk=course.program.pk)

    return render(request, "course/course_add.html", {
        "title": "Edit Course",
        "form": form,
        "course": course
    })


# ========================
# DELETE COURSE
# ========================
@login_required
@admin_required
def course_delete(request, pk):
    course = get_object_or_404(Course, pk=pk)
    program_id = course.program.id
    title = course.title

    course.delete()  # django-cleanup handles file deletion

    messages.success(request, f"{title} deleted successfully.")
    return redirect("program_detail", pk=program_id)


# ========================
# COURSE DETAILS
# ========================

@login_required
def course_details(request, pk):
    user = request.user
    course = get_object_or_404(Course, pk=pk)

    # Files
    files = CourseDocument.objects.filter(course=course)

    # Videos (ORDER IMPORTANT)
    videos = CourseVideo.objects.filter(course=course).order_by("no")

    # Progress
    progress_qs = VideoWatchProgress.objects.filter(
        employee=user,
        video__in=videos
    )
    progress_map = {p.video_id: p for p in progress_qs}

    # ✅ Udemy-style logic
    video_data = []
    unlock_next = True   # first video unlocked

    for video in videos:
        progress = progress_map.get(video.id)

        watched_seconds = progress.watched_duration if progress else 0
        completed = progress.watched if progress else False

        percent = round(
            (watched_seconds / video.duration) * 100, 2
        ) if video.duration else 0

        # ✅ SUPERUSER BYPASS
        if user.is_superuser:
            locked = False
        else:
            locked = not unlock_next

        video_data.append({
            "video": video,
            "percent": percent,
            "completed": completed,
            "locked": locked
        })

        # 🔒 lock next if not completed
        if not completed:
            unlock_next = False

    # ✅ Quiz unlock
    all_completed = all(v["completed"] for v in video_data)

    return render(request, "course/course_details.html", {
        "course": course,
        "files": files,
        "video_data": video_data,   # ✅ IMPORTANT (use this in template)
        "all_completed": all_completed,
    })
    
 
# ========================
# COURSE Video Upload
# ========================
@login_required
@admin_required
def course_video_upload(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = UploadVideo(request.POST, request.FILES)
        if form.is_valid():
            video = form.save(commit=False)
            video.course = course   # ✅ ForeignKey set here
            video.save()

            messages.success(request, f"{video.title} uploaded successfully.")
            return redirect("course_details", pk=pk)
    else:
        form = UploadVideo()

    return render(request, "upload/upload_video_form.html", {
        "title": "Upload Video",
        "form": form,
        "course": course,
    })
    
    
@login_required
@admin_required   
def course_video_edit(request, pk, video_id):
    course = get_object_or_404(Course, pk=pk)
    video = get_object_or_404(CourseVideo, pk=video_id)

    if request.method == 'POST':
        form = UploadVideo(request.POST, request.FILES, instance=video)

        if form.is_valid():
            obj = form.save(commit=False)

            # ✅ Ensure FK is always correct
            obj.course = course  

            # ✅ Delete old video if new one uploaded
            if request.FILES.get("video") and video.video:
                video.video.delete(save=False)

            obj.save()

            messages.success(request, f"{obj.title} updated successfully.")
            return redirect("course_details", pk=pk)
    else:
        form = UploadVideo(instance=video)

    return render(request, "upload/upload_video_form.html", {
        "title": "Edit Video",
        "form": form,
        "course": course,
    })
    
    
@login_required
@admin_required
def course_video_delete(request, pk, video_id):
    course = get_object_or_404(Course, pk=pk)

    # ✅ Ensure video belongs to this course
    video = get_object_or_404(CourseVideo, pk=video_id, course=course)

    title = video.title

    # ✅ Delete file safely
    if video.video:
        video.video.delete(save=False)

    video.delete()

    messages.success(request, f"{title} deleted successfully.")
    return redirect("course_details", pk=pk)


# ========================
# COURSE Document Upload
# ========================
@login_required
@admin_required
def course_file_upload(request, pk):
    course = get_object_or_404(Course, pk=pk)

    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)

            # ✅ set ForeignKey manually
            obj.course = course
            obj.save()

            messages.success(request, f"{obj.title} uploaded successfully.")
            return redirect("course_details", pk=pk)
    else:
        form = UploadFile()

    return render(request, "upload/upload_file_form.html", {
        "title": "Upload File",
        "form": form,
        "course": course,
    })
    
    
@login_required
@admin_required
def course_file_edit(request, pk, file_id):
    course = get_object_or_404(Course, pk=pk)

    # ✅ restrict file to this course
    file = get_object_or_404(CourseDocument, pk=file_id, course=course)

    if request.method == 'POST':
        form = UploadFile(request.POST, request.FILES, instance=file)

        if form.is_valid():
            obj = form.save(commit=False)

            # ✅ ensure FK is correct
            obj.course = course

            # ✅ delete old file if new uploaded
            if request.FILES.get("file") and file.file:
                file.file.delete(save=False)

            obj.save()

            messages.success(request, f"{obj.title} updated successfully.")
            return redirect("course_details", pk=pk)
    else:
        form = UploadFile(instance=file)

    return render(request, "upload/upload_file_form.html", {
        "title": "Edit File",
        "form": form,
        "course": course,
    })
    

@login_required
@admin_required
def course_file_delete(request, pk, file_id):
    course = get_object_or_404(Course, pk=pk)

    # ✅ restrict file to this course
    file = get_object_or_404(CourseDocument, pk=file_id, course=course)

    title = file.title

    # ✅ delete file from storage
    if file.file:
        file.file.delete(save=False)

    file.delete()

    messages.success(request, f"{title} deleted successfully.")
    return redirect("course_details", pk=pk)


# ========================
# Watch Video Sections
# ========================
@login_required
@staff_required
def video_played(request, course_id, video_id):
    if request.method != "POST":
        return JsonResponse({"status": "fail", "error": "Invalid request method"}, status=400)

    try:
        data = json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"status": "fail", "error": "Invalid JSON"}, status=400)

    # ---------------- GET DATA ----------------
    course = get_object_or_404(Course, id=course_id)
    video = get_object_or_404(CourseVideo, id=video_id, course=course)
    user = request.user

    watched_seconds = float(data.get("watched_seconds", 0))

    # ---------------- PROGRESS ----------------
    progress, _ = VideoWatchProgress.objects.get_or_create(
        employee=user,
        video=video
    )

    # ---------------- PREVENT BACKWARD OVERWRITE ----------------
    if watched_seconds > progress.watched_duration:
        progress.watched_duration = watched_seconds

    # ---------------- PERCENT CALCULATION ----------------
    percent = 0
    if video.duration and video.duration > 0:
        percent = (progress.watched_duration / video.duration) * 100

    # ---------------- VIDEO COMPLETION ----------------
    if percent >= 90:
        progress.watched = True

    progress.save()

    # ---------------- COURSE PROGRESS CHECK ----------------
    total_videos = CourseVideo.objects.filter(course=course).count()
    completed_videos = VideoWatchProgress.objects.filter(
        employee=user,
        video__course=course,
        watched=True
    ).count()

    all_completed = (total_videos > 0 and completed_videos == total_videos)

    # ---------------- CHECK NEXT VIDEO ----------------
    next_video = CourseVideo.objects.filter(
        course=course,
        no__gt=video.no
    ).order_by("no").first()

    return JsonResponse({
        "status": "success",
        "watched_seconds": progress.watched_duration,
        "watched_percent": round(percent, 2),
        "completed": progress.watched,
        "all_completed": all_completed,
        "video_id": video.id,
        "video_no": video.no,
        "next_video_id": next_video.id if next_video else None
    })
    
    

@login_required
@staff_required
def handle_video_single(request, course_id, video_id):
    user = request.user

    #  Get course & current video
    course = get_object_or_404(Course, id=course_id)
    current_video = get_object_or_404(CourseVideo, id=video_id, course=course)

    #  Order videos properly
    all_videos = CourseVideo.objects.filter(course=course).order_by('no')

    #  Files
    files = CourseDocument.objects.filter(course=course)

    #  Get progress
    progress_qs = VideoWatchProgress.objects.filter(
        employee=user,
        video__in=all_videos
    )

    progress_map = {p.video_id: p for p in progress_qs}

    #  Build video data
    video_data = []
    unlock_next = True
    completed_count = 0   

    for v in all_videos:
        progress = progress_map.get(v.id)

        watched_seconds = progress.watched_duration if progress else 0
        completed = progress.watched if progress else False

        #  safe percent
        percent = 0
        if v.duration and v.duration > 0:
            percent = round((watched_seconds / v.duration) * 100, 2)

        if completed:
            completed_count += 1

        video_data.append({
            "video": v,
            "percent": percent,
            "completed": completed,
            "locked": not unlock_next
        })

        #  lock next if not completed
        if not completed:
            unlock_next = False

    #  Resume Current Video Time
    current_progress = progress_map.get(current_video.id)
    resume_time = current_progress.watched_duration if current_progress else 0

    #  STRICT COMPLETE CHECK
    total_videos = all_videos.count()
    all_completed = (completed_count == total_videos and total_videos > 0)

    context = {
        'course': course,
        'video': current_video,
        'video_data': video_data,
        'files': files,
        'resume_time': resume_time,
        'all_completed': all_completed,
    }

    return render(request, 'upload/video_single.html', context)


# ==========================================
# REQUEST COURSE ACCESS
# ==========================================
from django.utils import timezone

@login_required
@login_required
def request_course_access(request, course_id):
    if request.method != "POST":
        return redirect("/")

    course = get_object_or_404(Course, id=course_id)
    User = get_user_model()

    # --------------------------------------------------
    # GET NOTIFICATION USERS (ADMINS / RECEIVERS)
    # --------------------------------------------------
    notification_record = SendEmailToReceiveUsers.objects.first()

    if notification_record:
        users = notification_record.users.filter(is_active=True)
    else:
        users = User.objects.filter(is_superuser=True, is_active=True)

    # --------------------------------------------------
    # ADMIN LINK
    # --------------------------------------------------
    admin_link = request.build_absolute_uri(
        reverse("admin:course_course_change", args=[course.pk])
    )

    # --------------------------------------------------
    # GET OR CREATE ALLOCATION (ONE ROW PER EMPLOYEE)
    # --------------------------------------------------
    allocation, created = CourseAllocation.objects.get_or_create(
        employee=request.user,
        courses=course,
        defaults={
            "status": "PENDING",
            "created_on": timezone.now(),
        }
    )

    if not created:
        allocation.status = "PENDING"
        allocation.save()

    # --------------------------------------------------
    # NOTIFICATIONS + EMAIL
    # --------------------------------------------------
    full_name = request.user.get_full_name or request.user.username

    for user in users:
        Notification.objects.create(
            sender=request.user,
            receiver=user,
            message=f"{full_name} requested access to '{course.title}'",
            url=admin_link,
        )

        if user.email:
            try:
                send_mail_notification(
                    to_emails=[user.email],
                    subject=f"Course Access Request: {course.title}",
                    body=f"{full_name} requested access",
                    html_message=render_to_string(
                        "emails/course_access_request.html",
                        {
                            "user": request.user,
                            "course": course,
                            "admin_link": admin_link,
                            "now": timezone.now(),
                        },
                    ),
                    request=request,
                )
            except Exception as e:
                print("Email error:", e)

    messages.success(request, "Request sent (PENDING approval).")
    return redirect("program_detail", pk=course.program.pk)
