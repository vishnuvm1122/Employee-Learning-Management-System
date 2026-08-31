from django.core.exceptions import ValidationError
from django.db import models


def validate_apk(value):
    if not value.name.lower().endswith(".apk"):
        raise ValidationError("Only APK files are allowed.")


class AndroidApp(models.Model):
    version_name = models.CharField(
        max_length=20,
        help_text="Example: 1.0.0"
    )

    version_code = models.PositiveIntegerField(
        unique=True,
        help_text="Example: 1, 2, 3..."
    )

    apk = models.FileField(
        upload_to="android_apk/",
        validators=[validate_apk],
        help_text="Upload APK file"
    )

    apk_size = models.CharField(
        max_length=20,
        blank=True,
        editable=False
    )

    force_update = models.BooleanField(
        default=False,
        help_text="Force users to update."
    )

    release_notes = models.TextField(
        blank=True
    )

    is_active = models.BooleanField(
        default=False
    )

    download_count = models.PositiveIntegerField(
        default=0
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ["-version_code"]
        verbose_name = "Android App"
        verbose_name_plural = "Android Apps"

    def __str__(self):
        return f"{self.version_name}"

    def clean(self):
        if self.is_active:
            qs = AndroidApp.objects.filter(
                is_active=True
            ).exclude(pk=self.pk)

            if qs.exists():
                raise ValidationError(
                    "Only one Android App version can be active."
                )

    def calculate_apk_size(self):
        if not self.apk:
            return ""

        try:
            size = self.apk.size

            if size >= 1024 * 1024 * 1024:
                return f"{size / (1024 * 1024 * 1024):.2f} GB"

            if size >= 1024 * 1024:
                return f"{size / (1024 * 1024):.2f} MB"

            if size >= 1024:
                return f"{size / 1024:.2f} KB"

            return f"{size} Bytes"

        except Exception:
            return ""

    def save(self, *args, **kwargs):
        self.full_clean()

        self.apk_size = self.calculate_apk_size()

        super().save(*args, **kwargs)

        if self.is_active:
            AndroidApp.objects.exclude(pk=self.pk).update(is_active=False)
