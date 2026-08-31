from functools import wraps
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required


# 🔐 Login required

# 👤 Staff required
def staff_required(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)

        messages.error(request, "You do not have permission.")
        return redirect('login')
    return wrapper


# 👑 Superuser required (ADMIN)
def admin_required(view_func):   # ✅ THIS FIXES YOUR ERROR
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_superuser:
            return view_func(request, *args, **kwargs)

        messages.error(request, "Admin access only.")
        return redirect('login')
    return wrapper


