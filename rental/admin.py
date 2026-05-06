from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin

from .models import User, Car, Rental, Invoice


@admin.register(User)
class UserAdmin(DjangoUserAdmin):
    list_display = (
        "username",
        "email",
        "role",
        "is_customer",
        "is_agent",
        "is_admin",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_customer",
        "is_agent",
        "is_admin",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "first_name",
        "last_name",
    )

    fieldsets = DjangoUserAdmin.fieldsets + (
        (
            "BérAutó jogosultságok és adatok",
            {
                "fields": (
                    "role",
                    "is_customer",
                    "is_agent",
                    "is_admin",
                    "phone_number",
                    "address",
                )
            },
        ),
    )

    add_fieldsets = DjangoUserAdmin.add_fieldsets + (
        (
            "BérAutó jogosultságok és adatok",
            {
                "fields": (
                    "role",
                    "phone_number",
                    "address",
                )
            },
        ),
    )


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = (
        "brand",
        "model",
        "year",
        "license_plate",
        "mileage",
        "daily_price",
        "available",
    )

    list_filter = (
        "available",
        "brand",
        "year",
    )

    search_fields = (
        "brand",
        "model",
        "license_plate",
    )


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "car",
        "customer",
        "agent",
        "start_date",
        "end_date",
    )

    list_filter = (
        "status",
        "start_date",
        "end_date",
    )

    search_fields = (
        "car__brand",
        "car__model",
        "car__license_plate",
        "customer__username",
        "agent__username",
    )


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "rental",
        "amount",
        "issued_date",
        "paid",
    )

    list_filter = (
        "paid",
        "issued_date",
    )

    search_fields = (
        "rental__car__brand",
        "rental__car__model",
        "rental__customer__username",
    )