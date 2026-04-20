from rest_framework.viewsets import ModelViewSet
from rest_framework.decorators import action
from rest_framework.response import Response
from django.utils.timezone import now

from ..models import Car, Rental, Invoice
from .serializers import CarSerializer, RentalSerializer, InvoiceSerializer
from .permissions import IsCustomer, IsAgent, IsAdmin

#car api
class CarViewSet(ModelViewSet):
    queryset = Car.objects.all()
    serializer_class = CarSerializer

#rental api
class RentalViewSet(ModelViewSet):
    queryset = Rental.objects.all()
    serializer_class = RentalSerializer

    def perform_create(self, serializer):
        serializer.save(customer=self.request.user)

    def get_queryset(self):
        user = self.request.user

        if user.role == "customer":
            return Rental.objects.filter(customer=user)
        return Rental.objects.all()
    
    #approve
    @action(detail=True, methods=["post"], permission_classes=[IsAgent])
    def approve(self, request, pk=None):
        rental = self.get_object()
        rental.status = "APPROVED"
        rental.approved_at = now()
        rental.agent = request.user
        rental.save()
        return Response({"status": "approved"})

    #reject
    @action(detail=True, methods=["post"], permission_classes=[IsAgent])
    def reject(self, request, pk=None):
        rental = self.get_object()
        rental.status = "REJECTED"
        rental.agent = request.user
        rental.save()
        return Response({"status": "rejected"})

    #handover
    @action(detail=True, methods=["post"], permission_classes=[IsAgent])
    def handover(self, request, pk=None):
        rental = self.get_object()
        rental.status = "HANDED_OVER"
        rental.handed_over_at = now()
        rental.car.available = False
        rental.car.save()
        rental.save()
        return Response({"status": "handed over"})

    #return
    @action(detail=True, methods=["post"], permission_classes=[IsAgent])
    def return_car(self, request, pk=None):
        rental = self.get_object()
        rental.status = "RETURNED"
        rental.returned_at = now()
        rental.car.available = True
        rental.car.save()
        rental.save()
        return Response({"status": "returned"})
    
    #invoice
class InvoiceViewSet(ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer

    @action(detail=True, methods=["post"], permission_classes=[IsAgent])
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