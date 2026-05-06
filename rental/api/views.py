from django.db import transaction
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet

from ..models import Car, Rental, Invoice
from .serializers import CarSerializer, RentalSerializer, InvoiceSerializer
from .permissions import CarPermission, RentalPermission, InvoicePermission

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from django.contrib.auth import get_user_model
from .serializers import RegisterSerializer
from drf_spectacular.utils import extend_schema

User = get_user_model()

class RegisterView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(request=RegisterSerializer)
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save()
            return Response(
                {"message": "Sikeres regisztráció"},
                status=status.HTTP_201_CREATED
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    

class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CarPermission]


class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.select_related("car", "customer", "agent").all()
    serializer_class = RentalSerializer
    permission_classes = [RentalPermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Rental.objects.select_related("car", "customer", "agent")

        if user.role == "customer":
            return queryset.filter(customer=user)

        return queryset

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "A kölcsönzés közvetlen módosítása nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "A kölcsönzés közvetlen módosítása nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "A kölcsönzés törlése nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=True, methods=["post"])
    def approve(self, request, pk=None):
        rental = self.get_object()
        rental.transition_to(Rental.Status.APPROVED, agent=request.user)
        return Response({"status": rental.status})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        rental = self.get_object()
        rental.transition_to(Rental.Status.REJECTED, agent=request.user)
        return Response({"status": rental.status})

    @action(detail=True, methods=["post"])
    def handover(self, request, pk=None):
        rental = self.get_object()

        with transaction.atomic():
            rental.car.available = False
            rental.car.save()
            rental.transition_to(Rental.Status.HANDED_OVER, agent=request.user)

        return Response({"status": rental.status})

    @action(detail=True, methods=["post"])
    def return_car(self, request, pk=None):
        rental = self.get_object()

        with transaction.atomic():
            rental.car.available = True
            rental.car.save()
            rental.transition_to(Rental.Status.RETURNED, agent=request.user)

        return Response({"status": rental.status})


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.select_related("rental", "rental__car", "rental__customer").all()
    serializer_class = InvoiceSerializer
    permission_classes = [InvoicePermission]

    def get_queryset(self):
        user = self.request.user
        queryset = Invoice.objects.select_related("rental", "rental__car", "rental__customer")

        if user.role == "customer":
            return queryset.filter(rental__customer=user)

        return queryset

    def create(self, request, *args, **kwargs):
        return Response(
            {"detail": "A számla közvetlen létrehozása nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def update(self, request, *args, **kwargs):
        return Response(
            {"detail": "A számla közvetlen módosítása nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def partial_update(self, request, *args, **kwargs):
        return Response(
            {"detail": "A számla közvetlen módosítása nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    def destroy(self, request, *args, **kwargs):
        return Response(
            {"detail": "A számla törlése nem engedélyezett."},
            status=status.HTTP_405_METHOD_NOT_ALLOWED,
        )

    @action(detail=True, methods=["post"])
    def pay(self, request, pk=None):
        invoice = self.get_object()

        if invoice.paid:
            return Response(
                {"detail": "Ez a számla már be van fizetve."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice.paid = True
        invoice.save(update_fields=["paid"])

        return Response({
            "message": "Sikeres befizetés.",
            "invoice_id": invoice.id,
            "paid": invoice.paid
        })

    @action(detail=True, methods=["post"])
    def generate(self, request, pk=None):
        rental = get_object_or_404(Rental, pk=pk)

        if rental.status != Rental.Status.RETURNED:
            return Response(
                {"detail": "Számla csak lezárt, visszavett bérléshez hozható létre."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        invoice = Invoice.objects.filter(rental=rental).first()

        if invoice is None:
            days = (rental.end_date - rental.start_date).days + 1
            amount = max(days, 1) * rental.car.daily_price

            invoice = Invoice.objects.create(
                rental=rental,
                amount=amount
            )

        return Response({
            "invoice_id": invoice.id,
            "amount": invoice.amount
        })