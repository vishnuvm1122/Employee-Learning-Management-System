from django.contrib import messages
from django.contrib.auth import get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.tokens import default_token_generator

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse

from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes

from django.template.loader import render_to_string

from accounts.decorators import admin_required
from accounts.forms import ProfileUpdateForm

from .forms import CustomPasswordResetForm
from emailsettings.utils import send_mail_notification
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView
from django.views import *
from django.contrib.auth import (
    get_user_model,
    login,
    update_session_auth_hash,
)


from .utils import (
    get_system_settings,
    send_email_2fa,
    save_user_otp,
    get_user_otp,
    delete_user_otp,
    verify_hashed_otp,
    get_client_ip,
    is_ip_allowed,
    is_ip_blocked,
    increase_ip_fail,
    clear_ip_fail,
    is_account_locked,
    increase_failed_attempt,
    reset_failed_attempt,
    can_resend_otp,
    create_security_log,
)


User = get_user_model()


# ########################################################
# AJAX - Username Validation
# ########################################################
def validate_username_email(request):
    username = (request.GET.get("username") or "").strip()
    email = (request.GET.get("email") or "").strip()

    username_taken = False
    email_taken = False

    # Check username
    if username:
        username_taken = User.objects.filter(username__iexact=username).exists()

    # Check email
    if email:
        email_taken = User.objects.filter(email__iexact=email).exists()

    return JsonResponse({
        "username_taken": username_taken,
        "email_taken": email_taken,
        "is_taken": username_taken or email_taken,
    })


# ########################################################
# Profile Views
# ########################################################
@login_required
def profile(request):
    user = request.user
    
    # Ensure we call the method, not treat it like a string
    if callable(getattr(user, "get_full_name", None)):
        full_name = user.get_full_name().strip()
    else:
        full_name = ""

    context = {
        "title": full_name if full_name else user.username,
    }
    return render(request, "accounts/profile.html", context)




@login_required
@admin_required
def admin_panel(request):
    return redirect('/admin/')


# ########################################################
# Settings
# ########################################################
@login_required
def profile_update(request):
    if request.method == "POST":
        form = ProfileUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = ProfileUpdateForm(instance=request.user)

    return render(request, "accounts/profile_info_change.html", {"form": form})


@login_required
def change_password(request):
    if request.method == "POST":
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # keep user logged in
            messages.success(request, "Password updated successfully.")
            return redirect("profile")
        messages.error(request, "Please correct the errors below.")
    else:
        form = PasswordChangeForm(request.user)

    return render(request, "accounts/password_change.html", {"form": form})



# ==========================================================
# PASSWORD RESET REQUEST
# ==========================================================

def password_reset_request(request):
    form = CustomPasswordResetForm()

    if request.method == "POST":
        form = CustomPasswordResetForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data["email"]
            user = User.objects.get(email=email)

            # 🔐 Generate token
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)

            # 🔗 Reset link
            reset_link = request.build_absolute_uri(
                reverse("password_reset_confirm", kwargs={
                    "uidb64": uid,
                    "token": token
                })
            )

            # 📧 Render HTML Email
            html_message = render_to_string(
                "emails/password_reset_email.html",
                {
                    "user": user,
                    "reset_link": reset_link
                }
            )

            # ✉️ Send using YOUR function
            send_mail_notification(
                to_emails=[user.email],
                subject="🔐 Password Reset Request",
                body=f"Click to reset password: {reset_link}",
                html_message=html_message,
                request=request
            )

            messages.success(request, "✅ Password reset link sent to your email.")
            return redirect("password_reset_done")

        else:
            messages.error(request, "⚠ Please enter a valid registered email.")

    return render(request, "registration/password_reset.html", {"form": form})






# ==========================================================
# MAINTENANCE PAGE
# ==========================================================
def maintenance_page(request):
    return render(
        request,
        "errors/maintenance.html"
    )


# ==========================================================
# CUSTOM LOGIN VIEW
# ==========================================================
class CustomLoginView(LoginView):

    template_name = "registration/login.html"
    redirect_authenticated_user = True

    # ------------------------------------------------------
    # BEFORE LOGIN
    # ------------------------------------------------------
    def dispatch(self, request, *args, **kwargs):

        settings_obj = get_system_settings()
        ip = get_client_ip(request)

        if (
            settings_obj.maintenance_mode
            and not request.user.is_superuser
        ):
            return render(
                request,
                "errors/maintenance.html"
            )

        if not is_ip_allowed(ip):
            messages.error(
                request,
                "Your IP is not allowed."
            )
            return redirect("login")

        if is_ip_blocked(ip):
            messages.error(
                request,
                "Too many attempts from your IP."
            )
            return redirect("login")

        return super().dispatch(
            request,
            *args,
            **kwargs
        )

    # ------------------------------------------------------
    # LOGIN SUCCESS
    # ------------------------------------------------------
    def form_valid(self, form):

        user = form.get_user()
        ip = get_client_ip(self.request)

        settings_obj = get_system_settings()

        if is_account_locked(user):
            messages.error(
                self.request,
                "Your account is locked."
            )
            return redirect("login")

        reset_failed_attempt(user)
        clear_ip_fail(ip)

        # 2FA LOGIN
        if settings_obj.enable_two_factor_auth:

            otp = send_email_2fa(user)

            save_user_otp(
                user.id,
                otp,
                ttl=120
            )

            self.request.session[
                "pending_user_id"
            ] = user.id

            self.request.session[
                "otp_attempts"
            ] = 0

            create_security_log(
                user=user.username,
                action="OTP_SENT",
                ip=ip,
                details="OTP login started"
            )

            messages.success(
                self.request,
                "OTP sent to email."
            )

            return redirect("verify_otp")

        # NORMAL LOGIN
        login(self.request, user)

        create_security_log(
            user=user.username,
            action="LOGIN_SUCCESS",
            ip=ip,
            details="Normal login"
        )

        return redirect("/")

    # ------------------------------------------------------
    # LOGIN FAILED
    # ------------------------------------------------------
    def form_invalid(self, form):

        username = self.request.POST.get("username")
        ip = get_client_ip(self.request)

        increase_ip_fail(ip)

        try:
            user = User.objects.get(
                username=username
            )
            increase_failed_attempt(user)

        except User.DoesNotExist:
            pass

        create_security_log(
            user=username,
            action="LOGIN_FAILED",
            ip=ip,
            details="Invalid credentials"
        )

        messages.error(
            self.request,
            "Invalid username or password."
        )

        return super().form_invalid(form)

    def get_success_url(self):
        return "/"


# ==========================================================
# VERIFY OTP VIEW
# ==========================================================
class VerifyOTPView(View):

    template_name = "registration/verify_otp.html"
    OTP_MAX_ATTEMPTS = 3

    # ------------------------------------------------------
    # GET
    # ------------------------------------------------------
    def get(self, request):
        return render(
            request,
            self.template_name
        )

    # ------------------------------------------------------
    # POST
    # ------------------------------------------------------
    def post(self, request):

        if "resend" in request.POST:
            return self.resend_otp(request)

        return self.verify_otp(request)

    # ------------------------------------------------------
    # VERIFY OTP
    # ------------------------------------------------------
    def verify_otp(self, request):

        user_id = request.session.get(
            "pending_user_id"
        )

        attempts = request.session.get(
            "otp_attempts",
            0
        )

        if not user_id:
            messages.error(
                request,
                "OTP session expired."
            )
            return redirect("login")

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            messages.error(
                request,
                "User not found."
            )
            return redirect("login")

        saved_hash = get_user_otp(user.id)

        if not saved_hash:
            messages.error(
                request,
                "OTP expired."
            )
            return redirect("login")

        entered_otp = request.POST.get(
            "otp",
            ""
        ).strip()

        # SUCCESS
        if verify_hashed_otp(
            entered_otp,
            saved_hash
        ):

            delete_user_otp(user.id)
            request.session.flush()

            login(request, user)

            create_security_log(
                user=user.username,
                action="OTP_SUCCESS",
                ip=get_client_ip(request),
                details="OTP verified"
            )

            messages.success(
                request,
                "Login successful."
            )

            return redirect("/")

        # FAILED
        attempts += 1
        request.session["otp_attempts"] = attempts

        if attempts >= self.OTP_MAX_ATTEMPTS:

            delete_user_otp(user.id)
            request.session.flush()

            create_security_log(
                user=user.username,
                action="OTP_FAILED_LIMIT",
                ip=get_client_ip(request),
                details="Too many wrong OTP"
            )

            messages.error(
                request,
                "Too many wrong OTP attempts."
            )

            return redirect("login")

        messages.error(
            request,
            f"Invalid OTP ({attempts}/3)"
        )

        return redirect("verify_otp")

    # ------------------------------------------------------
    # RESEND OTP
    # ------------------------------------------------------
    def resend_otp(self, request):

        user_id = request.session.get(
            "pending_user_id"
        )

        if not user_id:
            messages.error(
                request,
                "Session expired."
            )
            return redirect("login")

        try:
            user = User.objects.get(id=user_id)

        except User.DoesNotExist:
            messages.error(
                request,
                "User not found."
            )
            return redirect("login")

        if not can_resend_otp(user.id):
            messages.error(
                request,
                "Too many resend requests."
            )
            return redirect("verify_otp")

        otp = send_email_2fa(user)

        save_user_otp(
            user.id,
            otp,
            ttl=120
        )

        create_security_log(
            user=user.username,
            action="OTP_RESEND",
            ip=get_client_ip(request),
            details="OTP resent"
        )

        messages.success(
            request,
            "OTP resent successfully."
        )

        return redirect("verify_otp")
