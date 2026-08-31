from django.core.validators import FileExtensionValidator
from django.db import models
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.core.exceptions import ValidationError
from core.models import ActivityLog
from tinytag import TinyTag
from django.conf import settings
from django.core.files.base import ContentFile
import cv2
from PIL import Image
from io import BytesIO
import os


# ---------------- PROGRAM ----------------

class Program(models.Model):
    title = models.CharField(max_length=150, unique=True)
    summary = models.TextField(blank=True)
    photo = models.ImageField(upload_to='program_images/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("program_detail", kwargs={"pk": self.pk})


@receiver(post_save, sender=Program)
def log_program_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"Program '{instance}' {verb}.")


@receiver(post_delete, sender=Program)
def log_program_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"Program '{instance}' deleted.")


# ---------------- COURSE ----------------

LEVEL_CHOICES = (
    ('beginner', _("Beginner")),
    ('intermediate', _("Intermediate")),
    ('expert', _("Expert")),
)


class Course(models.Model):
    title = models.CharField(max_length=200)
    code = models.CharField(max_length=200, unique=True)
    photo = models.ImageField(upload_to='course_images/', null=True, blank=True)
    duration = models.PositiveIntegerField(default=0)
    summary = models.TextField(blank=True)
    program = models.ForeignKey(
        Program,
        on_delete=models.CASCADE,
        related_name="courses",
        null=True,
        blank=True
    )
    level = models.CharField(max_length=25, choices=LEVEL_CHOICES)

    class Meta:
        ordering = ['title']

    def __str__(self):
        return f"{self.title} ({self.code})"

    def get_absolute_url(self):
        return reverse("course_details", kwargs={"pk": self.pk})


@receiver(post_save, sender=Course)
def log_course_save(sender, instance, created, **kwargs):
    verb = "created" if created else "updated"
    ActivityLog.objects.create(message=f"Course '{instance}' {verb}.")


@receiver(post_delete, sender=Course)
def log_course_delete(sender, instance, **kwargs):
    ActivityLog.objects.create(message=f"Course '{instance}' deleted.")





# ---------------- COURSE DOCUMENTS ----------------

class CourseDocument(models.Model):
    title = models.CharField(max_length=100)
    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        related_name="documents"
    )
    file = models.FileField(
        upload_to="course_files/",
        validators=[FileExtensionValidator(
            ["pdf", "docx", "doc", "xls", "xlsx", "ppt", "pptx", "zip", "rar", "7z"]
        )],
    )
    updated_date = models.DateTimeField(auto_now=True)
    upload_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        if self.file:
            self.file.delete(save=False)
        super().delete(*args, **kwargs)


# ---------------- COURSE VIDEOS ----------------


class CourseVideo(models.Model):
    no = models.PositiveIntegerField(
        default=1,
        help_text="Video sequence number in the course"
    )

    title = models.CharField(max_length=100)

    course = models.ForeignKey(
        'Course',
        on_delete=models.CASCADE,
        related_name="videos"
    )

    video = models.FileField(
        upload_to="course_videos/",
        validators=[FileExtensionValidator(
            ["mp4", "mkv", "wmv", "3gp", "f4v", "avi"]
        )],
    )

    thumbnail = models.ImageField(
        upload_to="course_thumbnails/",
        blank=True,
        null=True
    )

    summary = models.TextField(blank=True)

    duration = models.FloatField(default=0.0)  # seconds

    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['course']),
        ]

    def __str__(self):
        return f"{self.no}. {self.title}"

    # ---------------- Video Duration ----------------
    def get_video_duration(self):
        try:
            if self.video and hasattr(self.video, 'path'):
                cap = cv2.VideoCapture(self.video.path)
                fps = cap.get(cv2.CAP_PROP_FPS)
                frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
                cap.release()
                if fps > 0:
                    return frame_count / fps
        except Exception as e:
            print("Duration error:", e)
        return 0.0

    # ---------------- Thumbnail Generation ----------------
    def generate_thumbnail(self):
        if self.video and hasattr(self.video, 'path'):
            cap = cv2.VideoCapture(self.video.path)

            frame_count = cap.get(cv2.CAP_PROP_FRAME_COUNT)
            middle_frame_number = int(frame_count // 2)
            cap.set(cv2.CAP_PROP_POS_FRAMES, middle_frame_number)

            success, frame = cap.read()
            cap.release()

            if success:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                img = Image.fromarray(frame)

                # Pillow ≥ 10.0 compatibility
                img.thumbnail((320, 180), Image.Resampling.LANCZOS)

                thumb_io = BytesIO()
                img.save(thumb_io, format='JPEG', quality=85)
                thumb_name = os.path.splitext(os.path.basename(self.video.name))[0] + "_thumb.jpg"
                self.thumbnail.save(thumb_name, ContentFile(thumb_io.getvalue()), save=False)

    # ---------------- Save ----------------
    def save(self, *args, **kwargs):
        is_new = self.pk is None
        super().save(*args, **kwargs)

        if is_new and self.video:
            # Update duration
            duration = self.get_video_duration()
            if duration:
                CourseVideo.objects.filter(pk=self.pk).update(duration=duration)

            # Generate thumbnail
            self.generate_thumbnail()
            super().save(update_fields=['thumbnail'])

    # ---------------- Delete ----------------
    def delete(self, *args, **kwargs):
        if self.video:
            self.video.delete(save=False)
        if self.thumbnail:
            self.thumbnail.delete(save=False)
        super().delete(*args, **kwargs)

    # ---------------- URL ----------------
    def get_absolute_url(self):
        return reverse("video_single", kwargs={
            "course_id": self.course.id,
            "video_id": self.id
        })

    # ---------------- Duration Display ----------------
    def get_duration_display(self):
        if not self.duration:
            return "0:00"
        minutes = int(self.duration // 60)
        seconds = int(self.duration % 60)
        return f"{minutes}:{seconds:02d}"

    # ---------------- Validation ----------------
    def clean(self):
        max_size = 1 * 1024 * 1024 * 1024  # 1 GB in bytes
        if self.video and self.video.size > max_size:
            raise ValidationError("Max file size is 1GB")
            
        
        
# ---------------- VIDEO PROGRESS ----------------

class VideoWatchProgress(models.Model):
    employee = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="video_progress"
    )
    video = models.ForeignKey(
        "CourseVideo",
        on_delete=models.CASCADE,
        related_name="watch_progress"
    )

    watched = models.BooleanField(default=False)  # ✅ means completed
    watched_duration = models.FloatField(default=0.0)
    last_watched_at = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ("employee", "video")
        ordering = ["-last_watched_at"]

    def __str__(self):
        return f"{self.employee} - {self.video}"

    def progress_percentage(self):
        if self.video.duration:
            return round((self.watched_duration / self.video.duration) * 100, 2)
        return 0

    # ✅ ADD THIS (important)
    def is_completed(self):
        return self.progress_percentage() >= 90