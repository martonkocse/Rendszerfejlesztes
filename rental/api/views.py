from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.viewsets import ModelViewSet
from django.utils.timezone import now

from ..models import Car, Rental, Invoice
from .serializers import CarSerializer, RentalSerializer, InvoiceSerializer
from .permissions import CarPermission, RentalPermission, InvoicePermission


class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer
    permission_classes = [CarPermission]


class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer
    permission_classes = [RentalPermission]

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            return Rental.objects.filter(customer=user)

        return Rental.objects.all()

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
        rental.status = "APPROVED"
        rental.approved_at = now()
        rental.agent = request.user
        rental.save()
        return Response({"status": "approved"})

    @action(detail=True, methods=["post"])
    def reject(self, request, pk=None):
        rental = self.get_object()
        rental.status = "REJECTED"
        rental.agent = request.user
        rental.save()
        return Response({"status": "rejected"})

    @action(detail=True, methods=["post"])
    def handover(self, request, pk=None):
        rental = self.get_object()
        rental.status = "HANDED_OVER"
        rental.handed_over_at = now()
        rental.car.available = False
        rental.car.save()
        rental.save()
        return Response({"status": "handed over"})

    @action(detail=True, methods=["post"])
    def return_car(self, request, pk=None):
        rental = self.get_object()
        rental.status = "RETURNED"
        rental.returned_at = now()
        rental.car.available = True
        rental.car.save()
        rental.save()
        return Response({"status": "returned"})


class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    permission_classes = [InvoicePermission]

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            return Invoice.objects.filter(rental__customer=user)

        return Invoice.objects.all()

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
    def generate(self, request, pk=None):
        rental = Rental.objects.get(pk=pk)

        days = (rental.end_date - rental.start_date).days
        amount = days * rental.car.daily_price

        invoice = Invoice.objects.create(
            rental=rental,
            amount=amount
        )

        return Response({
            "invoice_id": invoice.id,
            "amount": amount
        })