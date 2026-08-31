from django.contrib import admin
from django.utils.html import format_html
from .models import (
    Program,
    Course,
    CourseDocument,
    CourseVideo,
    VideoWatchProgress,
)


# ---------------- INLINE: DOCUMENT ----------------
class CourseDocumentInline(admin.TabularInline):
    model = CourseDocument
    extra = 0
    readonly_fields = ('upload_time', 'updated_date')


# ---------------- INLINE: VIDEO ----------------
class CourseVideoInline(admin.TabularInline):
    model = CourseVideo
    extra = 0
    readonly_fields = ('no', 'duration', 'timestamp', 'thumbnail_tag')
    fields = ('no', 'title', 'video', 'thumbnail_tag', 'duration', 'timestamp')

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="120" style="object-fit:cover;"/>', obj.thumbnail.url
            )
        return "-"
    thumbnail_tag.short_description = "Thumbnail"


# ---------------- INLINE: COURSE ----------------
class CourseInline(admin.TabularInline):
    model = Course
    extra = 0
    show_change_link = True


# ---------------- PROGRAM ----------------
@admin.register(Program)
class ProgramAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'course_count')
    search_fields = ('title',)
    list_filter = ('created_at',)
    ordering = ('-created_at',)
    inlines = [CourseInline]

    def course_count(self, obj):
        return obj.courses.count()
    course_count.short_description = "Courses"


# ---------------- COURSE ----------------
@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'code', 'program', 'level', 'duration')
    search_fields = ('title', 'code', 'program__title')
    list_filter = ('level', 'program')
    ordering = ('title',)
    list_select_related = ('program',)
    inlines = [CourseDocumentInline, CourseVideoInline]




# ---------------- DOCUMENT ADMIN ----------------
@admin.register(CourseDocument)
class CourseDocumentAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'upload_time', 'updated_date')
    search_fields = ('title', 'course__title')
    list_filter = ('upload_time',)
    list_select_related = ('course',)


# ---------------- VIDEO ADMIN ----------------
@admin.register(CourseVideo)
class CourseVideoAdmin(admin.ModelAdmin):
    list_display = ('no', 'title', 'course', 'thumbnail_tag', 'duration', 'timestamp')
    search_fields = ('title', 'course__title')
    list_filter = ('timestamp',)
    readonly_fields = ('no', 'duration', 'timestamp', 'thumbnail_tag')
    list_select_related = ('course',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return format_html(
                '<img src="{}" width="120" style="object-fit:cover;"/>', obj.thumbnail.url
            )
        return "-"
    thumbnail_tag.short_description = "Thumbnail"


# ---------------- VIDEO PROGRESS ----------------
@admin.register(VideoWatchProgress)
class VideoWatchProgressAdmin(admin.ModelAdmin):
    list_display = (
        'employee',
        'video',
        'watched',
        'watched_duration',
        'last_watched_at'
    )
    list_filter = ('watched', 'last_watched_at')
    search_fields = ('employee__username', 'video__title')
    list_select_related = ('employee', 'video')