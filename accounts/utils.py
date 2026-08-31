# utils.py

import secrets
import hashlib
from datetime import timedelta

from django.utils import timezone
from django.contrib.auth import logout
from django.template.loader import render_to_string
from django.core.cache import cache
from django.conf import settings

from emailsettings.utils import send_mail_notification
from .models import SystemSettings


# =====================================================
# GET SYSTEM SETTINGS
# =====================================================
def get_system_settings():
    """
    Load single settings row.
    Auto create if missing.
    """
    obj, created = SystemSettings.objects.get_or_create(pk=1)
    return obj


# =====================================================
# SECURE RANDOM OTP
# =====================================================
def generate_otp(length=6):
    """
    Generate secure numeric OTP.
    """
    digits = "0123456789"
    return "".join(secrets.choice(digits) for _ in range(length))


# =====================================================
# HASH OTP
# =====================================================
def hash_otp(otp):
    return hashlib.sha256(str(otp).encode()).hexdigest()


# =====================================================
# VERIFY HASHED OTP
# =====================================================
def verify_hashed_otp(raw_otp, hashed_otp):
    return hash_otp(raw_otp) == hashed_otp


# =====================================================
# SEND EMAIL OTP
# =====================================================
def send_email_2fa(user):
    """
    Send OTP email.
    Return raw OTP.
    """
    settings_obj = get_system_settings()

    if not settings_obj.enable_two_factor_auth:
        return None

    if not user.email:
        return None

    otp = generate_otp()

    html_message = render_to_string(
        "emails/otp_email.html",
        {
            "user": user,
            "otp": otp,
            "site_name": getattr(settings, "SITE_NAME", "System"),
            "year": timezone.now().year,
        }
    )

    send_mail_notification(
        to_emails=[user.email],
        subject="Your Verification Code",
        body=f"Your OTP code is {otp}",
        html_message=html_message
    )

    return otp


# =====================================================
# CACHE OTP
# =====================================================
def save_user_otp(user_id, otp, ttl=120):
    """
    Save hashed OTP in cache.
    """
    cache.set(
        f"otp_{user_id}",
        hash_otp(otp),
        timeout=ttl
    )


def get_user_otp(user_id):
    return cache.get(f"otp_{user_id}")


def delete_user_otp(user_id):
    cache.delete(f"otp_{user_id}")


# =====================================================
# MAINTENANCE MODE
# ====================================================

def is_maintenance_mode():
    return get_system_settings().maintenance_mode

# =====================================================
# SESSION TIMEOUT
# =====================================================
def is_session_expired(last_activity):
    if not last_activity:
        return False

    settings_obj = get_system_settings()

    expire_at = last_activity + timedelta(
        minutes=settings_obj.session_timeout_minutes
    )

    return timezone.now() > expire_at


# =====================================================
# FORCE LOGOUT
# =====================================================
def logout_user(request):
    logout(request)


# =====================================================
# GET CLIENT IP
# =====================================================
def get_client_ip(request):
    x_forwarded = request.META.get("HTTP_X_FORWARDED_FOR")

    if x_forwarded:
        return x_forwarded.split(",")[0].strip()

    return request.META.get("REMOTE_ADDR")


# =====================================================
# IP CHECK
# =====================================================
def is_ip_allowed(ip_address):
    settings_obj = get_system_settings()

    if not settings_obj.login_ip_restriction:
        return True

    allowed_ips = settings_obj.allowed_ips or ""

    ip_list = [
        ip.strip()
        for ip in allowed_ips.split(",")
        if ip.strip()
    ]

    return ip_address in ip_list


# =====================================================
# PASSWORD EXPIRY
# =====================================================
def is_password_expired(user):
    settings_obj = get_system_settings()

    if not user.last_login:
        return False

    expiry_date = user.last_login + timedelta(
        days=settings_obj.password_expiry_days
    )

    return timezone.now() > expiry_date


# =====================================================
# ACCOUNT LOCK
# =====================================================
def is_account_locked(user):
    settings_obj = get_system_settings()

    failed_attempts = getattr(user, "failed_login_attempts", 0)
    locked_at = getattr(user, "locked_at", None)

    if failed_attempts < settings_obj.max_login_attempts:
        return False

    if not locked_at:
        return False

    unlock_at = locked_at + timedelta(
        minutes=settings_obj.lock_account_duration_minutes
    )

    return timezone.now() < unlock_at


# =====================================================
# FAILED LOGIN ATTEMPT
# =====================================================
def increase_failed_attempt(user):
    settings_obj = get_system_settings()

    current = getattr(user, "failed_login_attempts", 0)
    user.failed_login_attempts = current + 1

    if user.failed_login_attempts >= settings_obj.max_login_attempts:
        user.locked_at = timezone.now()

    user.save(update_fields=["failed_login_attempts", "locked_at"])


# =====================================================
# RESET FAILED LOGIN
# =====================================================
def reset_failed_attempt(user):
    user.failed_login_attempts = 0
    user.locked_at = None
    user.save(update_fields=["failed_login_attempts", "locked_at"])


# =====================================================
# LOGIN SESSION LIMIT
# =====================================================
def can_user_login(active_sessions_count):
    settings_obj = get_system_settings()

    if settings_obj.allow_multiple_login:
        return True

    return active_sessions_count < settings_obj.max_login_sessions


# =====================================================
# SINGLE DEVICE LOGIN
# =====================================================
def enforce_single_device():
    return get_system_settings().force_single_device_login


# =====================================================
# FORCE LOGOUT OTHER SESSIONS
# =====================================================
def force_logout_others():
    return get_system_settings().force_logout_other_sessions


# =====================================================
# RATE LIMIT LOGIN BY IP
# =====================================================
def increase_ip_fail(ip):
    key = f"fail_ip_{ip}"
    count = cache.get(key, 0) + 1
    cache.set(key, count, timeout=600)
    return count


def clear_ip_fail(ip):
    cache.delete(f"fail_ip_{ip}")


def is_ip_blocked(ip, max_attempts=5):
    count = cache.get(f"fail_ip_{ip}", 0)
    return count >= max_attempts


# =====================================================
# RATE LIMIT OTP RESEND
# =====================================================
def can_resend_otp(user_id, limit=3):
    key = f"otp_resend_{user_id}"
    count = cache.get(key, 0)

    if count >= limit:
        return False

    cache.set(key, count + 1, timeout=300)
    return True


# =====================================================
# AUDIT LOG PLACEHOLDER
# =====================================================
def create_security_log(user=None, action="", ip="", details=""):
    print(
        f"[SECURITY] "
        f"user={user} "
        f"action={action} "
        f"ip={ip} "
        f"details={details}"
    )


# =====================================================
# REMEMBER DEVICE TOKEN
# =====================================================
def generate_device_token():
    return secrets.token_urlsafe(32)