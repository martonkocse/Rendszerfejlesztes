from rest_framework import serializers
from django.contrib.auth import get_user_model
from ..helpers import is_car_available
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
    agent = UserSerializer(read_only=True)
    car = CarSerializer(read_only=True)

    car_id = serializers.PrimaryKeyRelatedField(
        queryset=Car.objects.all(),
        write_only=True,
        source="car"
    )

    class Meta:
        model = Rental
        fields = [
            "id",
            "car",
            "car_id",
            "customer",
            "agent",
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
            "agent",
            "approved_at",
            "handed_over_at",
            "returned_at",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        validated_data["status"] = Rental.Status.PENDING
        return super().create(validated_data)

    def validate(self, data):
        instance = getattr(self, "instance", None)

        car = data.get("car") or getattr(instance, "car", None)
        start = data.get("start_date") or getattr(instance, "start_date", None)
        end = data.get("end_date") or getattr(instance, "end_date", None)

        if car and start and end:
            exclude_rental_id = instance.id if instance else None

            if not is_car_available(
                car=car,
                start_date=start,
                end_date=end,
                exclude_rental_id=exclude_rental_id,
            ):
                raise serializers.ValidationError(
                    "Ez az autó ebben az időszakban nem foglalható."
                )

        return data


class InvoiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invoice
        fields = "__all__"

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = [
            "username",
            "password",
            "first_name",
            "last_name",
            "email",
        ]

    def create(self, validated_data):
        return User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            first_name=validated_data.get("first_name", ""),
            last_name=validated_data.get("last_name", ""),
            email=validated_data.get("email", ""),
            role="customer",
        )