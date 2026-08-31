from django.db import models
from django.urls import reverse
from django.contrib.auth.models import AbstractUser, UserManager
from django.conf import settings
from django.utils.translation import gettext_lazy as _
from django.db.models import Q
from PIL import Image
from course.models import Program
from django.contrib.auth.validators import ASCIIUsernameValidator
from django.utils.timezone import now
from django.core.validators import MinLengthValidator
from datetime import timedelta

# -------------------------------
# USER MANAGER
# -------------------------------
class CustomUserManager(UserManager):
    def search(self, query=None):
        queryset = self.get_queryset()
        if query:
            queryset = queryset.filter(
                Q(username__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(email__icontains=query)
            ).distinct()
        return queryset

    def get_employee_count(self):
        return self.filter(is_superuser=False).count()

    def get_superuser_count(self):
        return self.filter(is_superuser=True).count()


# -------------------------------
# USER MODEL
# -------------------------------
GENDERS = (
    ("M", _("Male")),
    ("F", _("Female")),
)


class User(AbstractUser):
    username_validator = ASCIIUsernameValidator()

    # Custom fields
    division = models.CharField(max_length=60, blank=True, null=True)
    department = models.CharField(max_length=60, blank=True, null=True)
    reporting_manager = models.CharField(max_length=60, blank=True, null=True)
    group = models.CharField(max_length=60, blank=True, null=True)

    gender = models.CharField(max_length=1, choices=GENDERS, blank=True, null=True)
    phone = models.CharField(max_length=20, blank=True, null=True)
    nine_box_score = models.IntegerField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    date_of_joining = models.DateField(blank=True, null=True)

    failed_login_attempts = models.PositiveIntegerField(default=0)
    locked_at = models.DateTimeField(blank=True, null=True)


    picture = models.ImageField(
        upload_to="profile_pictures/%y/%m/%d/",
        blank=True,
        null=True,
    )

    email = models.EmailField(unique=True, blank=True, null=True)

    objects = CustomUserManager()

    class Meta:
        ordering = ("-date_joined",)

    def __str__(self):
        return f"{self.username} ({self.get_full_name})"

    @property
    def get_full_name(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    def get_picture(self):
        """
        Returns the URL of the user's profile picture.
        Uses MEDIA_URL for uploaded pictures.
        Falls back to STATIC_URL for default image.
        """
        if self.picture and hasattr(self.picture, "url"):
            return self.picture.url
        return settings.STATIC_URL + "img/default.png"

    def get_absolute_url(self):
        return reverse("profile_single", kwargs={"user_id": self.id})

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.picture:
            try:
                img = Image.open(self.picture.path)
                if img.height > 300 or img.width > 300:
                    img.thumbnail((300, 300))
                    img.save(self.picture.path)
            except Exception:
                pass

    def delete(self, *args, **kwargs):
        # Delete uploaded picture if not default
        if self.picture and self.picture.name != "default.png":
            self.picture.delete(save=False)
        super().delete(*args, **kwargs)




# -------------------------------
# LoginLogoutDeviceLog
# -------------------------------
class LoginLogoutDeviceLog(models.Model):
    STATUS_CHOICES = (
        ("ACTIVE", "Active"),
        ("LOGOUT", "Logout"),
        ("EXPIRED", "Expired"),
        ("FAILED", "Failed Login"),
        ("FORCED", "Forced Logout"),
    )

    DEVICE_TYPES = (
        ("Desktop", "Desktop"),
        ("Mobile", "Mobile"),
        ("Tablet", "Tablet"),
        ("Bot", "Bot"),
        ("Unknown", "Unknown"),
    )

    # -------------------------------------------------
    # USER
    # -------------------------------------------------
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="login_logs"
    )

    # -------------------------------------------------
    # NETWORK INFO
    # -------------------------------------------------
    ip_address = models.GenericIPAddressField(
        blank=True,
        null=True
    )

    mac_address = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # LOCATION INFO
    # -------------------------------------------------
    country = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    state = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    city = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    timezone_name = models.CharField(
        max_length=100,
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # DEVICE INFO
    # -------------------------------------------------
    screen_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    device_name = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    device_type = models.CharField(
        max_length=20,
        choices=DEVICE_TYPES,
        default="Unknown"
    )

    browser = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    browser_version = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    operating_system = models.CharField(
        max_length=120,
        blank=True,
        null=True
    )

    os_version = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )

    user_agent = models.TextField(
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # SESSION INFO
    # -------------------------------------------------
    session_key = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    login_time = models.DateTimeField(
        default=now,
        db_index=True
    )

    logout_time = models.DateTimeField(
        blank=True,
        null=True
    )

    last_activity = models.DateTimeField(
	auto_now=True,
	null=True, 
	blank=True
    )

    remember_me = models.BooleanField(
        default=False
    )

    # -------------------------------------------------
    # STATUS
    # -------------------------------------------------
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="ACTIVE",
        db_index=True
    )

    login_success = models.BooleanField(
        default=True
    )

    failed_reason = models.CharField(
        max_length=255,
        blank=True,
        null=True
    )

    remarks = models.TextField(
        blank=True,
        null=True
    )

    # -------------------------------------------------
    # SECURITY
    # -------------------------------------------------
    is_trusted_device = models.BooleanField(
        default=False
    )

    is_new_device = models.BooleanField(
        default=True
    )

    suspicious_login = models.BooleanField(
        default=False
    )

    multiple_session = models.BooleanField(
        default=False
    )

    # -------------------------------------------------
    # META
    # -------------------------------------------------
    class Meta:
        ordering = ["-login_time"]
        verbose_name = "Login Device Log"
        verbose_name_plural = "Login Device Logs"
        indexes = [
            models.Index(fields=["user"]),
            models.Index(fields=["status"]),
            models.Index(fields=["ip_address"]),
            models.Index(fields=["login_time"]),
        ]

    # -------------------------------------------------
    # STRING
    # -------------------------------------------------
    def __str__(self):
        return f"{self.user.username} - {self.ip_address} - {self.status}"

    # -------------------------------------------------
    # PROPERTIES
    # -------------------------------------------------
    @property
    def is_active(self):
        return self.status == "ACTIVE"

    @property
    def session_duration(self):
        if self.logout_time:
            return self.logout_time - self.login_time
        return now() - self.login_time

    @property
    def online_minutes(self):
        return int(self.session_duration.total_seconds() / 60)

    # -------------------------------------------------
    # METHODS
    # -------------------------------------------------
    def mark_logout(self):
        self.logout_time = now()
        self.status = "LOGOUT"
        self.save(update_fields=["logout_time", "status"])

    def mark_expired(self):
        self.logout_time = now()
        self.status = "EXPIRED"
        self.save(update_fields=["logout_time", "status"])

    def force_logout(self):
        self.logout_time = now()
        self.status = "FORCED"
        self.save(update_fields=["logout_time", "status"])

    def mark_failed(self, reason=None):
        self.status = "FAILED"
        self.login_success = False
        self.failed_reason = reason
        self.save()

    def is_idle(self, minutes=30):
        return self.last_activity < now() - timedelta(minutes=minutes)

    # -------------------------------------------------
    # SAVE
    # -------------------------------------------------
    def save(self, *args, **kwargs):

        # check multiple active sessions
        if self.user_id and self.status == "ACTIVE":
            active_exists = LoginLogoutDeviceLog.objects.filter(
                user=self.user,
                status="ACTIVE"
            ).exclude(pk=self.pk).exists()

            if active_exists:
                self.multiple_session = True

        super().save(*args, **kwargs)



# =====================================================
# SYSTEM SETTINGS
# =====================================================
class SystemSettings(models.Model):
    """
    Global application settings.
    Keep only one record.
    """

    # LOGIN CONTROL
    allow_multiple_login = models.BooleanField(default=True)
    max_login_sessions = models.PositiveIntegerField(default=3)

    force_single_device_login = models.BooleanField(default=False)
    force_logout_other_sessions = models.BooleanField(default=False)

    session_timeout_minutes = models.PositiveIntegerField(default=30)

    login_ip_restriction = models.BooleanField(default=False)

    allowed_ips = models.TextField(
        blank=True,
        null=True,
        help_text="Comma separated IPs. Example: 127.0.0.1,192.168.1.10"
    )

    # SECURITY
    enable_two_factor_auth = models.BooleanField(default=False)
    password_expiry_days = models.PositiveIntegerField(default=90)
    max_login_attempts = models.PositiveIntegerField(default=5)
    lock_account_duration_minutes = models.PositiveIntegerField(default=15)

    # SYSTEM
    maintenance_mode = models.BooleanField(default=False)

    # META
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "System Setting"
        verbose_name_plural = "System Settings"

    def __str__(self):
        return "System Settings"

    def save(self, *args, **kwargs):
        if not self.pk and SystemSettings.objects.exists():
            raise ValueError("Only one SystemSettings instance allowed.")

        super().save(*args, **kwargs)