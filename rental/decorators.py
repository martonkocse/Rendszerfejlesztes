from functools import wraps
from django.http import JsonResponse


def login_required_json(view_func):
    @wraps(view_func)
    def wrapper(request, *args, **kwargs):
        if not request.user.is_authenticated:
            return JsonResponse(
                {"success": False, "message": "Bejelentkezés szükséges."},
                status=401,
            )
        return view_func(request, *args, **kwargs)
    return wrapper


def role_required(allowed_roles):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return JsonResponse(
                    {"success": False, "message": "Bejelentkezés szükséges."},
                    status=401,
                )

            if request.user.role not in allowed_roles:
                return JsonResponse(
                    {"success": False, "message": "Nincs jogosultságod ehhez a művelethez."},
                    status=403,
                )

            return view_func(request, *args, **kwargs)
        return wrapper
    return decorator