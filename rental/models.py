from django.db import models
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
    mileage = models.IntegerField()
    daily_price = models.IntegerField(default=15000)
    available = models.BooleanField(default=True)

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

        if self.start_date and self.end_date:
            if self.start_date >= self.end_date:
                raise ValidationError(
                    {"end_date": "A záró dátumnak későbbinek kell lennie, mint a kezdő dátum."}
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

    def save(self, *args, **kwargs):
        self.full_clean()

        now = timezone.now()

        if self.status == self.Status.APPROVED and self.approved_at is None:
            self.approved_at = now

        if self.status == self.Status.HANDED_OVER and self.handed_over_at is None:
            self.handed_over_at = now

        if self.status == self.Status.RETURNED and self.returned_at is None:
            self.returned_at = now

        super().save(*args, **kwargs)

        if self.status == self.Status.RETURNED:
            days = (self.end_date - self.start_date).days + 1
            if days < 1:
                days = 1

            amount = days * self.car.daily_price

            Invoice.objects.get_or_create(
                rental=self,
                defaults={"amount": amount},
            )


class Invoice(models.Model):
    rental = models.OneToOneField(Rental, on_delete=models.CASCADE)
    amount = models.IntegerField()
    issued_date = models.DateField(auto_now_add=True)
    paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Invoice #{self.id} (rental {self.rental_id})"