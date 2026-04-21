from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.db.models import Q
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
        read_only_fields = [
            "status",
            "customer",
            "approved_at",
            "handed_over_at",
            "returned_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["status"] = "PENDING"
        return super().create(validated_data)
    def validate(self, data):
        car = data.get("car")
        start = data.get("start_date")
        end = data.get("end_date")

        # csak create-nél ellenőrizzük
        if car and start and end:
            overlapping = Rental.objects.filter(
                car=car
            ).filter(
                Q(start_date__lt=end) & Q(end_date__gt=start)
            )

            if overlapping.exists():
                raise serializers.ValidationError(
                    "Ez az autó már foglalt ebben az időszakban."
                )

        return data


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"