from django.contrib import admin
from .models import User, Car, Rental, Invoice


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("username", "email", "role", "is_customer", "is_agent", "is_admin")
    list_filter = ("role", "is_customer", "is_agent", "is_admin")
    search_fields = ("username", "email")


@admin.register(Car)
class CarAdmin(admin.ModelAdmin):
    list_display = ("brand", "model", "year", "mileage", "daily_price", "available")
    list_filter = ("available", "brand", "year")
    search_fields = ("brand", "model")


@admin.register(Rental)
class RentalAdmin(admin.ModelAdmin):
    list_display = ("id", "status", "car", "customer", "agent", "start_date", "end_date")
    list_filter = ("status", "start_date", "end_date")
    search_fields = ("car__brand", "car__model", "customer__username", "agent__username")


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = ("id", "rental", "amount", "issued_date", "paid")