from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('i18n/', include('django.conf.urls.i18n')),

    path("", include("core.urls")),
    path("accounts/", include("accounts.urls")),
    path("programs/", include("course.urls")),
    path("quiz/", include("quiz.urls")),
    path("courseallocations/", include("courseallocations.urls")),
    path("results/", include("results.urls")),
    path("search/", include("search.urls")),
    path("email/", include("emailsettings.urls")),
    path("notifications/", include("notifications.urls")),
    path("feedback/", include("feedback.urls")),
    path("android/", include("android.urls")),
]

# ✅ CUSTOM ERROR HANDLERS (MUST BE HERE)
handler404 = "core.views.custom_404"
handler500 = "core.views.custom_500"
handler403 = "core.views.custom_403"
handler400 = "core.views.custom_400"


# ✅ DEV ONLY
if settings.DEBUG:
    urlpatterns += [
        path("400/", default_views.bad_request, kwargs={"exception": Exception("Bad Request!")}),
        path("403/", default_views.permission_denied, kwargs={"exception": Exception("Permission Denied")}),
        path("404/", default_views.page_not_found, kwargs={"exception": Exception("Page Not Found")}),
        path("500/", default_views.server_error),
    ]

    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)