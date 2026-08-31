# accounts/middleware.py

from django.shortcuts import redirect
from django.contrib.auth import logout
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.urls import reverse
from django.contrib import messages

from .utils import (
    is_maintenance_mode,
    is_session_expired,
    get_client_ip,
    is_ip_allowed,
    create_security_log,
)


# ======================================================
# 1. MAINTENANCE MODE
# ======================================================

class MaintenanceModeMiddleware:

    def __init__(self, get_response):

        self.get_response = get_response



    def __call__(self, request):



        # Allow admin

        if request.path.startswith("/admin/"):

            return self.get_response(request)



        # Allow maintenance page (IMPORTANT FIX)

        if request.path.startswith("/accounts/maintenance/"):

            return self.get_response(request)





        # Allow superuser (optional)

        if request.user.is_authenticated and request.user.is_superuser:

            return self.get_response(request)



        # Redirect if maintenance ON

        if is_maintenance_mode():

            return redirect("maintenance_page")



        return self.get_response(request)





# ======================================================
# 2. SESSION TIMEOUT
# ======================================================
class SessionTimeoutMiddleware:
    """
    Auto logout inactive users, but bypasses expiration for the Eka Android App.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            user_agent = request.META.get("HTTP_USER_AGENT", "")

            # If the request comes from your Android WebView, bypass the timeout check entirely
            if "ekaapp" in user_agent.lower():
                return self.get_response(request)

            # Standard session timeout logic for desktop and normal mobile browsers
            last_activity = request.session.get("last_activity")

            if last_activity:
                last_activity = parse_datetime(last_activity)

                if is_session_expired(last_activity):

                    create_security_log(
                        user=request.user,
                        action="SESSION_EXPIRED",
                        ip=get_client_ip(request),
                        details="Auto logout due to inactivity",
                    )

                    logout(request)
                    messages.warning(request, "Session expired. Please login again.")
                    return redirect("login")

            request.session["last_activity"] = timezone.now().isoformat()

        return self.get_response(request)

# ======================================================
# 3. LOGIN IP RESTRICTION
# ======================================================
class LoginRestrictionMiddleware:
    """
    Restrict login by allowed IPs.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:

            ip = get_client_ip(request)

            if not is_ip_allowed(ip):

                create_security_log(
                    user=request.user,
                    action="BLOCKED_IP",
                    ip=ip,
                    details="Unauthorized IP blocked",
                )

                logout(request)
                messages.error(request, "Your IP address is not allowed.")
                return redirect("login")

        return self.get_response(request)


# ======================================================
# 4. AUDIT LOGGING
# ======================================================
class AuditMiddleware:
    """
    Log every request.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        if request.user.is_authenticated:
            create_security_log(
                user=request.user,
                action="PAGE_ACCESS",
                ip=get_client_ip(request),
                details=f"{request.method} {request.path}",
            )

        response = self.get_response(request)
        return response
