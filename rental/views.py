import json
from datetime import datetime

from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.http import require_GET, require_POST
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone

from .decorators import login_required_json, role_required
from .helpers import is_car_available
from .models import Car, Rental


User = get_user_model()

DATE_FORMAT = "%Y-%m-%d"


def home(request):
    return render(request, "rental/index.html")


def parse_json_body(request):
    try:
        return json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return None


def parse_date_value(value, field_name):
    try:
        return datetime.strptime(str(value), DATE_FORMAT).date()
    except (TypeError, ValueError):
        raise ValidationError({field_name: f"A(z) {field_name} mező formátuma YYYY-MM-DD legyen."})


def rental_to_dict(rental):
    return {
        "id": rental.id,
        "car": {
            "id": rental.car.id,
            "brand": rental.car.brand,
            "model": rental.car.model,
            "year": rental.car.year,
        },
        "customer": {
            "id": rental.customer.id,
            "username": rental.customer.username,
        },
        "agent": {
            "id": rental.agent.id,
            "username": rental.agent.username,
        } if rental.agent else None,
        "start_date": rental.start_date.isoformat(),
        "end_date": rental.end_date.isoformat(),
        "status": rental.status,
        "approved_at": rental.approved_at.isoformat() if rental.approved_at else None,
        "handed_over_at": rental.handed_over_at.isoformat() if rental.handed_over_at else None,
        "returned_at": rental.returned_at.isoformat() if rental.returned_at else None,
        "created_at": rental.created_at.isoformat(),
        "updated_at": rental.updated_at.isoformat(),
    }

@csrf_exempt
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

@csrf_exempt
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
@login_required_json
def car_list_view(request):
    start_date_raw = request.GET.get("start_date")
    end_date_raw = request.GET.get("end_date")

    start_date = None
    end_date = None

    if start_date_raw or end_date_raw:
        if not start_date_raw or not end_date_raw:
            return JsonResponse(
                {"success": False, "message": "A start_date és az end_date együtt kötelező."},
                status=400,
            )

        try:
            start_date = parse_date_value(start_date_raw, "start_date")
            end_date = parse_date_value(end_date_raw, "end_date")
        except ValidationError as e:
            return JsonResponse(
                {"success": False, "errors": e.message_dict},
                status=400,
            )

        if start_date > end_date:
            return JsonResponse(
                {"success": False, "message": "A kezdő dátum nem lehet későbbi a záró dátumnál."},
                status=400,
            )

    cars = Car.objects.all().order_by("brand", "model", "year")
    result = []

    for car in cars:
        reservable = car.available
        if start_date and end_date:
            reservable = is_car_available(car, start_date, end_date)

        result.append(
            {
                "id": car.id,
                "brand": car.brand,
                "model": car.model,
                "year": car.year,
                "mileage": car.mileage,
                "daily_price": car.daily_price,
                "active": car.available,
                "reservable": reservable,
            }
        )

    return JsonResponse({"success": True, "cars": result})


@require_GET
@login_required_json
def car_availability_view(request, car_id):
    start_date_raw = request.GET.get("start_date")
    end_date_raw = request.GET.get("end_date")

    if not start_date_raw or not end_date_raw:
        return JsonResponse(
            {"success": False, "message": "A start_date és az end_date kötelező."},
            status=400,
        )

    try:
        start_date = parse_date_value(start_date_raw, "start_date")
        end_date = parse_date_value(end_date_raw, "end_date")
    except ValidationError as e:
        return JsonResponse(
            {"success": False, "errors": e.message_dict},
            status=400,
        )

    if start_date > end_date:
        return JsonResponse(
            {"success": False, "message": "A kezdő dátum nem lehet későbbi a záró dátumnál."},
            status=400,
        )

    car = get_object_or_404(Car, id=car_id)
    reservable = is_car_available(car, start_date, end_date)

    return JsonResponse(
        {
            "success": True,
            "car_id": car.id,
            "active": car.available,
            "reservable": reservable,
            "start_date": start_date.isoformat(),
            "end_date": end_date.isoformat(),
        }
    )


@csrf_exempt
@require_POST
@login_required_json
def create_rental_view(request):
    data = parse_json_body(request)
    if data is None:
        return JsonResponse(
            {"success": False, "message": "Hibás JSON kérés."},
            status=400,
        )

    car_id = data.get("car")

    if not car_id:
        return JsonResponse(
            {
                "success": False,
                "errors": {
                    "car": ["A car mező kötelező."]
                },
            },
            status=400,
        )

    try:
        start_date = parse_date_value(data.get("start_date"), "start_date")
        end_date = parse_date_value(data.get("end_date"), "end_date")
    except ValidationError as e:
        return JsonResponse(
            {"success": False, "errors": e.message_dict},
            status=400,
        )

    today = timezone.localdate()

    if start_date < today:
        return JsonResponse(
            {
                "success": False,
                "errors": {
                    "start_date": ["A kezdő dátum nem lehet múltbeli."]
                },
            },
            status=400,
        )

    if end_date < today:
        return JsonResponse(
            {
                "success": False,
                "errors": {
                    "end_date": ["A záró dátum nem lehet múltbeli."]
                },
            },
            status=400,
        )

    if start_date >= end_date:
        return JsonResponse(
            {
                "success": False,
                "message": "A kezdő dátumnak korábbinak kell lennie, mint a záró dátum.",
            },
            status=400,
        )

    car = get_object_or_404(Car, id=car_id)

    if not is_car_available(car, start_date, end_date):
        return JsonResponse(
            {"success": False, "message": "Az autó a megadott időszakban nem foglalható."},
            status=409,
        )

    rental = Rental.objects.create(
        car=car,
        customer=request.user,
        start_date=start_date,
        end_date=end_date,
        status=Rental.Status.PENDING,
    )

    return JsonResponse(
        {
            "success": True,
            "message": "A bérlési igény rögzítve lett.",
            "rental": rental_to_dict(rental),
        },
        status=201,
    )


@csrf_exempt
@require_POST
@role_required([User.Role.AGENT, User.Role.ADMIN])
def update_rental_status_view(request, rental_id):
    data = parse_json_body(request)
    if data is None:
        return JsonResponse(
            {"success": False, "message": "Hibás JSON kérés."},
            status=400,
        )

    new_status = str(data.get("status", "")).strip().upper()
    allowed_statuses = {choice for choice, _ in Rental.Status.choices}

    if new_status not in allowed_statuses:
        return JsonResponse(
            {"success": False, "message": "Érvénytelen státusz."},
            status=400,
        )

    rental = get_object_or_404(Rental, id=rental_id)

    if new_status in {Rental.Status.APPROVED, Rental.Status.HANDED_OVER}:
        if not is_car_available(rental.car, rental.start_date, rental.end_date, exclude_rental_id=rental.id):
            return JsonResponse(
                {"success": False, "message": "Van már átfedő jóváhagyott vagy átadott bérlés erre az autóra."},
                status=409,
            )

    rental.status = new_status
    rental.agent = request.user
    rental.save()

    return JsonResponse(
        {
            "success": True,
            "message": "A bérlés státusza frissítve lett.",
            "rental": rental_to_dict(rental),
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


