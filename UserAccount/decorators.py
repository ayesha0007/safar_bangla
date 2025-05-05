from django.http import HttpResponseForbidden
from functools import wraps

def superuser_required(view_func):
    """
    Decorator to allow access only to superusers.
    """
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_superuser:
            return HttpResponseForbidden("You do not have permission to view this page.")
        return view_func(request, *args, **kwargs)
    return wrapper
