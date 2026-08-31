from django.urls import path, reverse_lazy
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [

    # =========================
    # 👤 USER PROFILE
    # =========================
    path("profile/", views.profile, name="profile"),
    path("setting/", views.profile_update, name="edit_profile"),
    path("change-password/", views.change_password, name="change_password"),
    path("admin-panel/", views.admin_panel, name="admin_panel"),

    # =========================
    # 🔐 AUTHENTICATION
    # =========================
    # path(
    #     "login/",
    #     auth_views.LoginView.as_view(
    #         template_name="registration/login.html",
    #         redirect_authenticated_user=True
    #     ),
    #     name="login",
    # ),

    path("maintenance/", views.maintenance_page, name="maintenance_page"),
    path("login/",views.CustomLoginView.as_view(redirect_authenticated_user=True),name="login",),
    path("verify-otp/", views.VerifyOTPView.as_view(), name="verify_otp"), 



    path(
        "logout/",
        auth_views.LogoutView.as_view(
            next_page=reverse_lazy("login")
        ),
        name="logout",
    ),

    # =========================
    # 🔍 AJAX VALIDATION
    # =========================
    path(
        "ajax/validate-email/",
        views.validate_username_email,
        name="validate_username_email",
    ),

    # =========================
    # 🔑 PASSWORD RESET FLOW (CUSTOM)
    # =========================

    # ✅ Step 1: CUSTOM VIEW (IMPORTANT CHANGE)
    path(
        "password-reset/",
        views.password_reset_request,   # ✅ YOUR CUSTOM VIEW
        name="password_reset",
    ),

    # Step 2: Email Sent Page
    path(
        "password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="registration/password_reset_done.html",
        ),
        name="password_reset_done",
    ),

    # Step 3: Reset Link (from email)
    path(
        "reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
            template_name="registration/password_reset_confirm.html",
            success_url=reverse_lazy("password_reset_complete"),
        ),
        name="password_reset_confirm",
    ),

    # Step 4: Success Page
    path(
        "reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="registration/password_reset_complete.html",
        ),
        name="password_reset_complete",
    ),
]