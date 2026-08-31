from django.contrib import admin
from django.utils.html import format_html
from .models import NewsAndEvents


@admin.register(NewsAndEvents)
class NewsAndEventsAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "posted_as",
        "image_preview",
        "updated_date",
        "upload_time",
    )

    list_filter = ("posted_as", "updated_date")
    search_fields = ("title", "summary")
    ordering = ("-upload_time",)

    readonly_fields = ("image_preview",)

    def image_preview(self, obj):
        if obj.photo:
            return format_html(
                '<img src="{}" width="60" height="60" style="object-fit:cover;" />',
                obj.photo.url
            )
        return "No Image"

    image_preview.short_description = "Preview"