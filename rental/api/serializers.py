from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..models import Car, Rental, Invoice

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "username", "email", "role", "phone_number", "address"]


class CarSerializer(serializers.ModelSerializer):
    class Meta:
        model = Car
        fields = "__all__"


class RentalSerializer(serializers.ModelSerializer):
    customer = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(), write_only=True, source="car"
    )

    class Meta:
        model = Rental
        fields = [
            "id",
            "car",
            "car_id",
            "customer",
            "start_date",
            "end_date",
            "status",
            "approved_at",
            "handed_over_at",
            "returned_at",
            "created_at",
            "updated_at",
        ]


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"