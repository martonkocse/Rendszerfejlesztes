from rest_framework.permissions import BasePermission, SAFE_METHODS


class IsCustomer(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "customer"
        )


class IsAgent(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role in ["agent", "admin"]
        )


class IsAdmin(BasePermission):
    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and request.user.role == "admin"
        )


class CarPermission(BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False

        if request.method in SAFE_METHODS:
            return True

        return request.user.role in ["agent", "admin"]


class RentalPermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if view.action in ["list", "retrieve"]:
            return user.role in ["customer", "agent", "admin"]

        if view.action == "create":
            return user.role == "customer"

        if view.action in ["approve", "reject", "handover", "return_car"]:
            return user.role in ["agent", "admin"]

        if view.action in ["update", "partial_update", "destroy"]:
            return False

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role in ["agent", "admin"]:
            return True

        if user.role == "customer":
            return obj.customer_id == user.id

        return False


class InvoicePermission(BasePermission):
    def has_permission(self, request, view):
        user = request.user

        if not user.is_authenticated:
            return False

        if view.action in ["list", "retrieve"]:
            return user.role in ["customer", "agent", "admin"]

        if view.action == "generate":
            return user.role in ["agent", "admin"]

        if view.action in ["create", "update", "partial_update", "destroy"]:
            return False

        return False

    def has_object_permission(self, request, view, obj):
        user = request.user

        if user.role in ["agent", "admin"]:
            return True

        if user.role == "customer":
            return obj.rental.customer_id == user.id

        return False