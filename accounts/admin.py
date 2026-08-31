
import logging
from django.contrib import admin, messages
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.templatetags.static import static
from django.urls import reverse
from django.utils import timezone
from django.utils.html import format_html
from import_export import fields, resources
from import_export.admin import ImportExportModelAdmin
from import_export.widgets import BooleanWidget, DateWidget
from .forms import UserAdminForm
from .models import *
from emailsettings.utils import send_mail_notification
import csv
from django.contrib import admin, messages
from django.http import HttpResponse
from django.utils.html import format_html
from .models import LoginLogoutDeviceLog
from django.utils.safestring import mark_safe
from django.contrib.sessions.models import Session


logger = logging.getLogger(__name__)
User = get_user_model()


# ==========================================================
# IMPORT / EXPORT RESOURCE
# ==========================================================
class UserResource(resources.ModelResource):
    username = fields.Field(column_name="Employee ID", attribute="username")
    first_name = fields.Field(column_name="First Name", attribute="first_name")
    last_name = fields.Field(column_name="Last Name", attribute="last_name")
    email = fields.Field(column_name="Email", attribute="email")
    phone = fields.Field(column_name="Phone", attribute="phone")

    is_active = fields.Field(
        column_name="Active",
        attribute="is_active",
        widget=BooleanWidget()
    )

    is_staff = fields.Field(
        column_name="Staff",
        attribute="is_staff",
        widget=BooleanWidget()
    )

    is_superuser = fields.Field(
        column_name="Superuser",
        attribute="is_superuser",
        widget=BooleanWidget()
    )

    gender = fields.Field(column_name="Gender", attribute="gender")
    department = fields.Field(column_name="Department", attribute="department")
    division = fields.Field(column_name="Division", attribute="division")
    nine_box_score = fields.Field(column_name="Nine Box Score", attribute="nine_box_score")
    reporting_manager = fields.Field(column_name="Reporting Manager", attribute="reporting_manager")

    date_of_joining = fields.Field(
        column_name="Date of Employee Joining",
        attribute="date_of_joining",
        widget=DateWidget(format="%Y-%m-%d")
    )

    password = fields.Field(column_name="Password", attribute="password")

    class Meta:
        model = User
        import_id_fields = ("username",)

        fields = (
            "username",
            "first_name",
            "last_name",
            "email",
            "phone",
            "is_active",
            "is_staff",
            "is_superuser",
            "gender",
            "department",
            "division",
            "nine_box_score",
            "reporting_manager",
            "date_of_joining",
            "password",
        )

        export_order = fields

    # ------------------------------------------------------
    # HASH PASSWORD ONLY FINAL IMPORT
    # ------------------------------------------------------
    def before_save_instance(self, instance, row=None, dry_run=False, **kwargs):
        if dry_run:
            return

        password = getattr(instance, "password", None)

        if password:
            password = str(password).strip()

            if not password.startswith("pbkdf2_"):
                instance.set_password(password)
    # ------------------------------------------------------
    # SEND EMAIL AFTER FINAL IMPORT
    # ------------------------------------------------------
    def after_import(self, dataset, result, using_transactions, dry_run, **kwargs):
        if dry_run:
            return

        request = kwargs.get("request")   # get request safely

        for row in dataset.dict:
            try:
                username = row.get("Employee ID")
                email = row.get("Email")
                password = row.get("Password", "")

                if not email:
                    continue

                user = User.objects.get(username=username)

                # Build login URL
                if request:
                    login_link = request.build_absolute_uri(reverse("login"))
                else:
                    login_link = reverse("login")

                html_message = render_to_string(
                    "emails/user_created.html",
                    {
                        "user": user,
                        "password": password,
                        "action": "created",
                        "login_link": login_link,
                        "now": timezone.now(),
                    }
                )

                send_mail_notification(
                    to_emails=[email],
                    subject="Your account has been created",
                    body=f"Username: {username}",
                    html_message=html_message,
                )

            except Exception as e:
                logger.error(f"Import email failed: {e}")



# ==========================================================
# USER ADMIN
# ==========================================================
@admin.register(User)
class UserAdmin(ImportExportModelAdmin):
    form = UserAdminForm
    resource_class = UserResource

    list_display = (
        "id",
        "picture_preview",
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "is_active",
        "is_staff",
        "is_superuser",
        "department",
        "division",
    )

    search_fields = (
        "username",
        "first_name",
        "last_name",
        "email",
        "phone",
        "department",
        "division",
    )

    list_filter = (
        "is_active",
        "is_staff",
        "is_superuser",
        "department",
        "division",
    )

    ordering = ("-date_joined",)

    readonly_fields = (
        "date_joined",
        "picture_preview",
    )

    fieldsets = (
        ("Login Information", {
            "fields": (
                "username",
                "password1",
                "password2",
            )
        }),

        ("Profile Photo", {
            "fields": (
                "picture",
                "picture_preview",
            )
        }),

        ("Personal Information", {
            "fields": (
                "first_name",
                "last_name",
                "email",
                "phone",
                "gender",
            )
        }),

        ("Organization", {
            "fields": (
                "department",
                "division",
                "reporting_manager",
            )
        }),

        ("Performance", {
            "classes": ("collapse",),
            "fields": ("nine_box_score",),
        }),

        ("Permissions", {
            "fields": (
                "is_active",
                "is_staff",
                "is_superuser",
            )
        }),

        ("Dates", {
            "fields": (
                "date_joined",
                "date_of_joining",
            )
        }),
    )

    add_fieldsets = (
        ("Create User", {
            "classes": ("wide",),
            "fields": (
                "username",
                "password1",
                "password2",
                "first_name",
                "last_name",
                "email",
                "phone",
                "gender",
                "department",
                "division",
                "reporting_manager",
                "is_active",
                "is_staff",
                "is_superuser",
                "picture",
            ),
        }),
    )

    # ------------------------------------------------------
    # IMAGE PREVIEW
    # ------------------------------------------------------
    def picture_preview(self, obj):
        if obj and obj.picture:
            return format_html(
                '<img src="{}" width="50" height="50" '
                'style="border-radius:50%;object-fit:cover;" />',
                obj.picture.url
            )

        return format_html(
            '<img src="{}" width="50" height="50" '
            'style="border-radius:50%;object-fit:cover;" />',
            static("profile/no_image.png")
        )

    picture_preview.short_description = "Photo"

    # ------------------------------------------------------
    # CREATE / UPDATE MAIL
    # ------------------------------------------------------
    def save_model(self, request, obj, form, change):
        is_new = obj._state.adding
        raw_password = form.cleaned_data.get("password1")

        if obj.is_superuser and not request.user.is_superuser:
            raise PermissionError("Only superuser can assign superuser role.")

        if obj.is_superuser:
            obj.is_staff = True

        super().save_model(request, obj, form, change)

        if obj.email:
            try:
                action = "created" if is_new else "updated"

                html_message = render_to_string(
                    "emails/user_created.html",
                    {
                        "user": obj,
                        "password": raw_password if is_new else None,
                        "action": action,
                        "login_link": request.build_absolute_uri(
                            reverse("login")
                        ),
                        "now": timezone.now(),
                    }
                )

                send_mail_notification(
                    to_emails=[obj.email],
                    subject=f"Your account has been {action}",
                    body=f"Username: {obj.username}",
                    html_message=html_message,
                    request=request,
                )

            except Exception as e:
                logger.error(f"Save email failed: {e}")

    # ------------------------------------------------------
    # SINGLE DELETE MAIL
    # ------------------------------------------------------
    def delete_model(self, request, obj):
        email = obj.email
        username = obj.username

        super().delete_model(request, obj)

        if email:
            try:
                html_message = render_to_string(
                    "emails/user_deleted.html",
                    {
                        "username": username,
                        "login_link": request.build_absolute_uri(
                            reverse("login")
                        ),
                        "now": timezone.now(),
                    }
                )

                send_mail_notification(
                    to_emails=[email],
                    subject="Your account has been deleted",
                    body=f"Your account ({username}) has been deleted.",
                    html_message=html_message,
                    request=request,
                )

            except Exception as e:
                logger.error(f"Delete email failed: {e}")

    # ------------------------------------------------------
    # MULTIPLE DELETE MAIL
    # ------------------------------------------------------
    def delete_queryset(self, request, queryset):
        users = list(queryset)

        for user in users:
            if user.email:
                try:
                    html_message = render_to_string(
                        "emails/user_deleted.html",
                        {
                            "username": user.username,
                            "login_link": request.build_absolute_uri(
                                reverse("login")
                            ),
                            "now": timezone.now(),
                        }
                    )

                    send_mail_notification(
                        to_emails=[user.email],
                        subject="Your account has been deleted",
                        body=f"Your account ({user.username}) has been deleted.",
                        html_message=html_message,
                        request=request,
                    )

                except Exception as e:
                    logger.error(f"Bulk delete email failed: {e}")

        queryset.delete()

        messages.success(
            request,
            "Selected users deleted and separate emails sent."
        )



# ==========================================================
# LOGIN LOG ADMIN (ADVANCED CLEAN VERSION)
# ==========================================================
@admin.register(LoginLogoutDeviceLog)
class LoginLogoutDeviceLogAdmin(admin.ModelAdmin):

    # ------------------------------------------------------
    # LIST VIEW
    # ------------------------------------------------------
    list_display = (
        "id",
        "full_name",
        "user",
        "status_badge",
        "live_badge",
        "ip_address",
        "location_display",
        "device_display",
        "browser_display",
        "os_display",
        "login_time",
        "logout_time",
        "duration_display",
    )

    search_fields = (
        "user__username",
        "user__first_name",
        "user__last_name",
        "user__email",
        "ip_address",
        "device_name",
        "browser",
        "operating_system",
        "country",
        "state",
        "city",
        "session_key",
    )

    list_filter = (
        "status",
        "device_type",
        "browser",
        "operating_system",
        "country",
        "login_success",
        "login_time",
    )

    ordering = ("-login_time",)
    list_per_page = 150
    list_select_related = ("user",)

    # ------------------------------------------------------
    # READONLY FIELDS
    # ------------------------------------------------------
    readonly_fields = (
        "user",
        "ip_address",
        "screen_name",
        "session_key",
        "status",
        "login_success",
        "device_name",
        "device_type",
        "browser",
        "browser_version",
        "operating_system",
        "os_version",
        "country",
        "state",
        "city",
        "timezone_name",
        "login_time",
        "logout_time",
        "last_activity",
        "remarks",
        "duration_display",
        "user_agent",
    )

    # ------------------------------------------------------
    # FIELDSETS
    # ------------------------------------------------------
    fieldsets = (
        ("User Info", {
            "fields": ("user", "status", "login_success", "remarks")
        }),
        ("Location", {
            "fields": ("ip_address", "country", "state", "city", "timezone_name")
        }),
        ("Device", {
            "fields": (
                "screen_name",
                "device_name",
                "device_type",
                "browser",
                "browser_version",
                "operating_system",
                "os_version",
            )
        }),
        ("Session", {
            "fields": (
                "session_key",
                "login_time",
                "logout_time",
                "last_activity",
                "duration_display",
            )
        }),
        ("Technical", {
            "classes": ("collapse",),
            "fields": ("user_agent",)
        }),
    )

    # ------------------------------------------------------
    # ACTIONS
    # ------------------------------------------------------
    actions = (
        "force_logout",
        "mark_as_logout",
        "mark_as_expired",
        "delete_logs",
        "export_csv",
    )

    # ======================================================
    # DISPLAY METHODS
    # ======================================================

    @admin.display(description="Full Name")
    def full_name(self, obj):
        if obj.user:
            name = f"{obj.user.first_name} {obj.user.last_name}".strip()
            return name if name else obj.user.username
        return "-"

    @admin.display(description="Status")
    def status_badge(self, obj):
        colors = {
            "ACTIVE": "#28a745",
            "LOGOUT": "#007bff",
            "FAILED": "#dc3545",
            "EXPIRED": "#ffc107",
            "FORCED": "#6f42c1",
        }
        color = colors.get(obj.status, "#6c757d")

        return format_html(
            '<span style="padding:4px 10px; border-radius:8px; color:white; background:{};">{}</span>',
            color,
            obj.status
        )

    @admin.display(description="Live")
    def live_badge(self, obj):
        if obj.status == "ACTIVE":
            return format_html(
                '<span style="padding:3px 8px; border-radius:8px; color:white; background:{};">{}</span>',
                "#28a745",
                "LIVE"
            )
        return "-"

    @admin.display(description="Location")
    def location_display(self, obj):
        values = [obj.city, obj.state, obj.country]
        return ", ".join([v for v in values if v]) or "-"

    @admin.display(description="Device")
    def device_display(self, obj):
        icons = {
            "Desktop": "",
            "Mobile": "",
            "Tablet": "",
            "Bot": "",
        }
        return f"{icons.get(obj.device_type, '')} {obj.device_name or '-'}"

    @admin.display(description="Browser")
    def browser_display(self, obj):
        return f"{obj.browser or '-'} {obj.browser_version or ''}".strip()

    @admin.display(description="OS")
    def os_display(self, obj):
        return f"{obj.operating_system or '-'} {obj.os_version or ''}".strip()

    @admin.display(description="Duration")
    def duration_display(self, obj):
        if obj.login_time and obj.logout_time:
            return str(obj.logout_time - obj.login_time).split(".")[0]

        if obj.login_time and obj.status == "ACTIVE":
            return str(timezone.now() - obj.login_time).split(".")[0]

        return "-"

    # ======================================================
    # ACTION METHODS
    # ======================================================

    @admin.action(description="Force logout selected sessions")
    def force_logout(self, request, queryset):

        updated_count = 0

        active_sessions = queryset.filter(status__iexact="ACTIVE")

        for obj in active_sessions:

            try:
                # Delete Django session
                if obj.session_key:
                    Session.objects.filter(
                        session_key=obj.session_key
                    ).delete()

                # Update log object
                obj.status = "FORCED"
                obj.logout_time = timezone.now()
                obj.last_activity = timezone.now()

                # Optional
                obj.is_online = False

                obj.save()

                updated_count += 1

            except Exception as e:
                print("Force logout error:", e)

        self.message_user(
            request,
            f"{updated_count} session(s) forcefully logged out successfully.",
            messages.SUCCESS
        )
        
    @admin.action(description="Mark selected as Logout")
    def mark_as_logout(self, request, queryset):

        updated = 0

        for obj in queryset.filter(status__iexact="ACTIVE"):

            try:

                # Delete Django session
                if obj.session_key:
                    Session.objects.filter(
                        session_key=obj.session_key
                    ).delete()

                # Update log model
                obj.status = "LOGOUT"
                obj.logout_time = timezone.now()
                obj.last_activity = timezone.now()

                # Optional online flag
                if hasattr(obj, "is_online"):
                    obj.is_online = False

                obj.save()

                updated += 1

            except Exception as e:
                print("Logout error:", e)

        self.message_user(
            request,
            f"{updated} session(s) marked as logout successfully.",
            messages.SUCCESS
        )

    @admin.action(description="Mark selected as Expired")
    def mark_as_expired(self, request, queryset):

        updated = 0

        for obj in queryset.filter(status__iexact="ACTIVE"):

            try:

                # Delete Django session
                if obj.session_key:
                    Session.objects.filter(
                        session_key=obj.session_key
                    ).delete()

                # Update log details
                obj.status = "EXPIRED"
                obj.logout_time = timezone.now()
                obj.last_activity = timezone.now()

                # Optional online status
                if hasattr(obj, "is_online"):
                    obj.is_online = False

                obj.save()

                updated += 1

            except Exception as e:
                print("Expire session error:", e)

        self.message_user(
            request,
            f"{updated} session(s) marked as expired successfully.",
            messages.WARNING
        )

    @admin.action(description="Delete selected logs")
    def delete_logs(self, request, queryset):
        count = queryset.count()
        queryset.delete()

        self.message_user(
            request,
            f"{count} log(s) deleted.",
            messages.ERROR
        )

    @admin.action(description="Export selected as CSV")
    def export_csv(self, request, queryset):

        response = HttpResponse(content_type="text/csv")
        response["Content-Disposition"] = 'attachment; filename="login_logs.csv"'

        writer = csv.writer(response)

        writer.writerow([
            "User", "IP", "Country", "State", "City",
            "Device", "Browser", "OS",
            "Status", "Login Time", "Logout Time"
        ])

        for obj in queryset:
            writer.writerow([
                obj.user.username if obj.user else "",
                obj.ip_address or "",
                obj.country or "",
                obj.state or "",
                obj.city or "",
                obj.device_name or "",
                obj.browser or "",
                obj.operating_system or "",
                obj.status or "",
                obj.login_time or "",
                obj.logout_time or "",
            ])

        return response

    def has_add_permission(self, request):
        return False


    def has_change_permission(self, request, obj=None):
        return False


    def has_delete_permission(self, request, obj=None):
        return True    


# =====================================================
# SYSTEM SETTINGS ADMIN
# =====================================================
@admin.register(SystemSettings)
class SystemSettingsAdmin(admin.ModelAdmin):

    list_display = (
        "system_status",
        "enable_two_factor_auth",
        "allow_multiple_login",
        "max_login_sessions",
        "session_timeout_minutes",
        "updated_at",
    )

    readonly_fields = (
        "dashboard_cards",
        "created_at",
        "updated_at",
    )

    fieldsets = (
        (" Dashboard", {
            "fields": ("dashboard_cards",)
        }),

        (" Login Control", {
            "fields": (
                "allow_multiple_login",
                "max_login_sessions",
                "force_single_device_login",
                "force_logout_other_sessions",
                "session_timeout_minutes",
            )
        }),

        (" Security", {
            "fields": (
                "enable_two_factor_auth",
                "password_expiry_days",
                "max_login_attempts",
                "lock_account_duration_minutes",
            )
        }),

        (" Network", {
            "fields": (
                "login_ip_restriction",
                "allowed_ips",
            )
        }),

        (" System", {
            "fields": (
                "maintenance_mode",
            )
        }),

        (" Logs", {
            "fields": (
                "created_at",
                "updated_at",
            )
        }),
    )

    def has_add_permission(self, request):
        return not SystemSettings.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False

    def system_status(self, obj):
        if obj.maintenance_mode:
            return " Maintenance"
        return " Running"

    def dashboard_cards(self, obj):
        return mark_safe(f"""
        <div style="display:grid;
                    grid-template-columns:repeat(4,1fr);
                    gap:15px;">

            <div style="background:#007bff;color:white;
                        padding:15px;border-radius:12px;">
                <h4>Sessions</h4>
                <h2>{obj.max_login_sessions}</h2>
            </div>

            <div style="background:#28a745;color:white;
                        padding:15px;border-radius:12px;">
                <h4>2FA</h4>
                <h2>{"ON" if obj.enable_two_factor_auth else "OFF"}</h2>
            </div>

            <div style="background:#6f42c1;color:white;
                        padding:15px;border-radius:12px;">
                <h4>Password Expiry</h4>
                <h2>{obj.password_expiry_days}</h2>
            </div>

            <div style="background:#dc3545;color:white;
                        padding:15px;border-radius:12px;">
                <h4>Maintenance</h4>
                <h2>{"ON" if obj.maintenance_mode else "OFF"}</h2>
            </div>

        </div>
        """)


# =====================================================
# ADMIN BRANDING
# =====================================================
admin.site.site_header = "LMS Security Dashboard"
admin.site.site_title = "LMS Admin"
admin.site.index_title = "Welcome to Advanced Control Panel"


