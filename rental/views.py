import json

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_GET, require_POST

from .decorators import login_required_json, role_required

User = get_user_model()


def home(request):
    return render(request, "rental/index.html")


def parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


@require_POST
def register_view(request):
    data = parse_json_body(request)
    if data is None:
        return JsonResponse(
            {"success": False, "message": "Hibás JSON kérés."},
            status=400,
        )

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()
    email = str(data.get("email", "")).strip()
    phone_number = str(data.get("phone_number", "")).strip()
    address = str(data.get("address", "")).strip()
    role = str(data.get("role", User.Role.CUSTOMER)).strip().lower()

    if not username or not password:
        return JsonResponse(
            {"success": False, "message": "A felhasználónév és a jelszó kötelező."},
            status=400,
        )

    allowed_roles = {User.Role.CUSTOMER, User.Role.AGENT, User.Role.ADMIN}
    if role not in allowed_roles:
        return JsonResponse(
            {"success": False, "message": "Érvénytelen szerepkör."},
            status=400,
        )

    if User.objects.filter(username=username).exists():
        return JsonResponse(
            {"success": False, "message": "Ez a felhasználónév már foglalt."},
            status=400,
        )

    if email and User.objects.filter(email=email).exists():
        return JsonResponse(
            {"success": False, "message": "Ez az email cím már használatban van."},
            status=400,
        )

    try:
        validate_password(password)
    except ValidationError as e:
        return JsonResponse(
            {"success": False, "message": list(e.messages)},
            status=400,
        )

    user = User.objects.create_user(
        username=username,
        password=password,
        email=email,
        phone_number=phone_number or None,
        address=address or None,
        role=role,
    )

    return JsonResponse(
        {
            "success": True,
            "message": "Sikeres regisztráció.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        },
        status=201,
    )


@require_POST
def login_view(request):
    data = parse_json_body(request)
    if data is None:
        return JsonResponse(
            {"success": False, "message": "Hibás JSON kérés."},
            status=400,
        )

    username = str(data.get("username", "")).strip()
    password = str(data.get("password", "")).strip()

    if not username or not password:
        return JsonResponse(
            {"success": False, "message": "A felhasználónév és a jelszó kötelező."},
            status=400,
        )

    user = authenticate(request, username=username, password=password)
    if user is None:
        return JsonResponse(
            {"success": False, "message": "Hibás felhasználónév vagy jelszó."},
            status=401,
        )

    login(request, user)

    return JsonResponse(
        {
            "success": True,
            "message": "Sikeres bejelentkezés.",
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
            },
        }
    )


@require_POST
@login_required_json
def logout_view(request):
    logout(request)
    return JsonResponse(
        {"success": True, "message": "Sikeres kijelentkezés."}
    )


@require_GET
@login_required_json
def me_view(request):
    user = request.user
    return JsonResponse(
        {
            "success": True,
            "user": {
                "id": user.id,
                "username": user.username,
                "email": user.email,
                "role": user.role,
                "phone_number": user.phone_number,
                "address": user.address,
            },
        }
    )


@require_GET
@role_required([User.Role.CUSTOMER])
def customer_only_view(request):
    return JsonResponse(
        {
            "success": True,
            "message": "Customer jogosultság rendben.",
            "user": request.user.username,
            "role": request.user.role,
        }
    )


@require_GET
@role_required([User.Role.AGENT])
def agent_only_view(request):
    return JsonResponse(
        {
            "success": True,
            "message": "Agent jogosultság rendben.",
            "user": request.user.username,
            "role": request.user.role,
        }
    )


@require_GET
@role_required([User.Role.ADMIN])
def admin_only_view(request):
    return JsonResponse(
        {
            "success": True,
            "message": "Admin jogosultság rendben.",
            "user": request.user.username,
            "role": request.user.role,
        }
    )


@require_GET
@role_required([User.Role.AGENT, User.Role.ADMIN])
def staff_only_view(request):
    return JsonResponse(
        {
            "success": True,
            "message": "Agent vagy admin jogosultság rendben.",
            "user": request.user.username,
            "role": request.user.role,
        }
    )