from django.contrib import admin
from .models import EmailSettings, SendEmailToReceiveUsers


@admin.register(EmailSettings)
class EmailSettingsAdmin(admin.ModelAdmin):
    list_display = (
        "host",
        "port",
        "username",
        "use_tls",
        "use_ssl",
        "email_enabled",
        "updated_at",
    )

    fieldsets = (
        ("SMTP Settings", {
            "fields": ("host", "port", "username", "password"),
        }),
        ("Security", {
            "fields": ("use_tls", "use_ssl"),
        }),
        ("Status", {
            "fields": ("email_enabled",),
        }),
    )

    # Only allow a single record
    def has_add_permission(self, request):
        return not EmailSettings.objects.exists()

    # Hide password field in admin
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        form.base_fields["password"].widget.input_type = "password"
        return form




@admin.register(SendEmailToReceiveUsers)
class SendEmailToReceiveUsersAdmin(admin.ModelAdmin):
    list_display = ("id", "created_at", "user_details")
    filter_horizontal = ("users",)
    readonly_fields = ("created_at",)

    # ==========================================
    # SHOW USER DETAILS (TEXT FORMAT)
    # ==========================================
    def user_details(self, obj):
        details = []

        for user in obj.users.all():
            full_name = (
                f"{user.first_name} {user.last_name}"
                if user.first_name or user.last_name
                else user.username
            )

            department = getattr(user, "department", "N/A")
            role = getattr(user, "role", "N/A")
            superuser = "Yes" if user.is_superuser else "No"
            active = "Yes" if user.is_active else "No"

            details.append(
                f"{full_name} | "
                f"Dept: {department} | "
                f"Role: {role} | "
                f"Superuser: {superuser} | "
                f"Active: {active}"
            )

        return "\n".join(details) if details else "-"

    user_details.short_description = "Selected Users"

    # ==========================================
    # ONLY ONE RECORD ALLOWED
    # HIDE ADD BUTTON AFTER ONE ENTRY
    # ==========================================
    def has_add_permission(self, request):
        return SendEmailToReceiveUsers.objects.count() == 0

    # ==========================================
    # DISABLE DELETE
    # ==========================================
    def has_delete_permission(self, request, obj=None):
        return False