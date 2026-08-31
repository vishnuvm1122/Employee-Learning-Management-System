# notifications/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Notification

# =========================
# 📋 Notification List Page
# =========================
@login_required
def notification_list(request):
    """
    Displays all notifications for the logged-in user,
    including counts for read, unread, and total notifications.
    """
    notifications = Notification.objects.filter(
        receiver=request.user
    ).order_by("-created_at")

    unread_count = notifications.filter(is_read=False).count()
    read_count = notifications.filter(is_read=True).count()
    total_count = notifications.count()

    # Optional: add href to notifications if needed
    for note in notifications:
        if not hasattr(note, 'href'):
            # Example: link to a detail page or mark as read URL
            note.href = f"/notifications/detail/{note.pk}/"

    context = {
        "notifications": notifications,
        "unread_count": unread_count,
        "read_count": read_count,
        "total_count": total_count,
    }

    return render(request, "notifications/list.html", context)


# =========================
# ✅ Mark Single Notification as Read
# =========================
@login_required
def mark_notification_read(request, pk):
    """
    Marks a single notification as read.
    Supports AJAX requests to update live count.
    """
    notification = get_object_or_404(Notification, pk=pk, receiver=request.user)
    notification.is_read = True
    notification.save()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
        return JsonResponse({"status": "success", "count": unread_count})

    return redirect("notifications:notification_list")


# =========================
# ❌ Delete Single Notification
# =========================
@login_required
def delete_notification(request, pk):
    """
    Deletes a single notification.
    Supports AJAX requests to update live count.
    """
    notification = get_object_or_404(Notification, pk=pk, receiver=request.user)
    notification.delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        unread_count = Notification.objects.filter(receiver=request.user, is_read=False).count()
        return JsonResponse({"status": "deleted", "count": unread_count})

    messages.success(request, "Notification deleted")
    return redirect("notifications:notification_list")


# =========================
# ✅ Mark All Notifications as Read
# =========================
@login_required
def mark_all_read(request):
    """
    Marks all unread notifications for the user as read.
    Supports AJAX requests.
    """
    Notification.objects.filter(receiver=request.user, is_read=False).update(is_read=True)

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": "all_read", "count": 0})

    messages.success(request, "All notifications marked as read")
    return redirect("notifications:notification_list")


# =========================
# ❌ Delete All Notifications
# =========================
@login_required
def delete_all_notifications(request):
    """
    Deletes all notifications for the user.
    Supports AJAX requests.
    """
    Notification.objects.filter(receiver=request.user).delete()

    if request.headers.get("x-requested-with") == "XMLHttpRequest":
        return JsonResponse({"status": "all_deleted", "count": 0})

    messages.success(request, "All notifications deleted")
    return redirect("notifications:notification_list")


# =========================
# 🔢 Live Unread Notification Count (AJAX)
# =========================
@login_required
def notification_count(request):
    """
    Returns the live unread notification count for the logged-in user.
    """
    count = Notification.objects.filter(receiver=request.user, is_read=False).count()
    return JsonResponse({"count": count})