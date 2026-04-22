from datetime import date

from .models import Rental


BLOCKING_STATUSES = [
    Rental.Status.PENDING,
    Rental.Status.APPROVED,
    Rental.Status.HANDED_OVER,
]


def is_car_available(car, start_date: date, end_date: date, exclude_rental_id=None) -> bool:
    if start_date > end_date:
        return False

    open_handover_exists = Rental.objects.filter(
        car=car,
        status=Rental.Status.HANDED_OVER,
        returned_at__isnull=True,
    )

    if exclude_rental_id is not None:
        open_handover_exists = open_handover_exists.exclude(id=exclude_rental_id)

    if open_handover_exists.exists():
        return False

    overlapping_rentals = Rental.objects.filter(
        car=car,
        status__in=BLOCKING_STATUSES,
        start_date__lte=end_date,
        end_date__gte=start_date,
    )

    if exclude_rental_id is not None:
        overlapping_rentals = overlapping_rentals.exclude(id=exclude_rental_id)

    return not overlapping_rentals.exists()