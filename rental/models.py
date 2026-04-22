from django.db import models, transaction
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.utils import timezone


class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "customer", "Customer"
        AGENT = "agent", "Agent"
        ADMIN = "admin", "Admin"

    role = models.CharField(
        max_length=20,
        choices=Role.choices,
        default=Role.CUSTOMER,
    )

    is_customer = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)

    phone_number = models.CharField(max_length=30, blank=True, null=True)
    address = models.CharField(max_length=255, blank=True, null=True)

    def save(self, *args, **kwargs):
        self.is_customer = self.role == self.Role.CUSTOMER
        self.is_agent = self.role == self.Role.AGENT
        self.is_admin = self.role == self.Role.ADMIN
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.username} ({self.role})"


class Car(models.Model):
    brand = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    year = models.IntegerField()
    license_plate = models.CharField(max_length=20, unique=True)
    mileage = models.IntegerField(default=0)
    daily_price = models.IntegerField(default=15000)
    available = models.BooleanField(default=True)

    def clean(self):
        super().clean()

        current_year = timezone.localdate().year

        if self.year < 1886 or self.year > current_year + 1:
            raise ValidationError({"year": "Érvénytelen évjárat."})

        if self.mileage < 0:
            raise ValidationError({"mileage": "A kilométeróra állás nem lehet negatív."})

        if self.daily_price <= 0:
            raise ValidationError({"daily_price": "A napi díjnak pozitív értéknek kell lennie."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.brand} {self.model} ({self.year})"


class Rental(models.Model):
    class Status(models.TextChoices):
        PENDING = "PENDING", "PENDING"
        APPROVED = "APPROVED", "APPROVED"
        REJECTED = "REJECTED", "REJECTED"
        HANDED_OVER = "HANDED_OVER", "HANDED_OVER"
        RETURNED = "RETURNED", "RETURNED"

    ALLOWED_TRANSITIONS = {
        Status.PENDING: {Status.APPROVED, Status.REJECTED},
        Status.APPROVED: {Status.HANDED_OVER},
        Status.HANDED_OVER: {Status.RETURNED},
        Status.REJECTED: set(),
        Status.RETURNED: set(),
    }

    car = models.ForeignKey(Car, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rentals")
    agent = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="processed_rentals",
    )

    start_date = models.DateField()
    end_date = models.DateField()

    status = models.CharField(
        max_length=20,
        choices=Status.choices,
        default=Status.PENDING,
    )

    approved_at = models.DateTimeField(null=True, blank=True)
    handed_over_at = models.DateTimeField(null=True, blank=True)
    returned_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        super().clean()

        if not self.car_id:
            raise ValidationError({"car": "Az autó megadása kötelező."})

        if not self.customer_id:
            raise ValidationError({"customer": "Az ügyfél megadása kötelező."})

        if self.agent_id and self.agent.role not in [User.Role.AGENT, User.Role.ADMIN]:
            raise ValidationError({"agent": "Csak ügyintéző vagy admin rendelhető a bérléshez."})

        if self.start_date and self.end_date:
            if self.start_date > self.end_date:
                raise ValidationError(
                    {"end_date": "A záró dátumnak legalább a kezdő dátummal egyezőnek kell lennie."}
                )

            today = timezone.localdate()

            if self.start_date < today:
                raise ValidationError(
                    {"start_date": "A kezdő dátum nem lehet múltbeli."}
                )

            if self.end_date < today:
                raise ValidationError(
                    {"end_date": "A záró dátum nem lehet múltbeli."}
                )

        if self.pk:
            old = Rental.objects.get(pk=self.pk)

            if old.status != self.status:
                allowed = self.ALLOWED_TRANSITIONS.get(old.status, set())

                if self.status not in allowed:
                    raise ValidationError(
                        {"status": f"Nem engedélyezett státuszváltás: {old.status} -> {self.status}"}
                    )

    def transition_to(self, new_status, *, agent=None):
        self.status = new_status

        if agent is not None:
            self.agent = agent

        self.save()

    def save(self, *args, **kwargs):
        self.full_clean()

        now = timezone.now()

        if self.status == self.Status.APPROVED and self.approved_at is None:
            self.approved_at = now

        if self.status == self.Status.HANDED_OVER and self.handed_over_at is None:
            self.handed_over_at = now

        if self.status == self.Status.RETURNED and self.returned_at is None:
            self.returned_at = now

        with transaction.atomic():
            super().save(*args, **kwargs)

            if self.status == self.Status.RETURNED:
                days = (self.end_date - self.start_date).days + 1
                amount = max(days, 1) * self.car.daily_price

                Invoice.objects.get_or_create(
                    rental=self,
                    defaults={"amount": amount},
                )

    def __str__(self):
        return f"#{self.id} - {self.car} - {self.customer}"

class Invoice(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE, related_name="invoice")
    amount = models.IntegerField()
    issued_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def clean(self):
        super().clean()

        if self.amount <= 0:
            raise ValidationError({"amount": "A számla összege nem lehet nulla vagy negatív."})

    def save(self, *args, **kwargs):
        self.full_clean()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Invoice #{self.id} (rental {self.rental_id})"