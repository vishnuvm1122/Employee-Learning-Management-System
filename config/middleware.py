# config/middleware.py
from django.shortcuts import redirect
from django.contrib import messages

class SuperuserAdminOnlyMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Check if user is trying to access /admin/
        if request.path.startswith('/admin/') and request.user.is_authenticated:
            if not request.user.is_superuser:
                # Add a message to show on home page
                messages.error(request, "Only superusers can access the admin panel.")
                # Redirect to home page
                return redirect('home')  # make sure 'home' is your home URL name
        return self.get_response(request)