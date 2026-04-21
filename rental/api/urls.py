from rest_framework.routers import DefaultRouter
from .views import CarViewSet, RentalViewSet, InvoiceViewSet

router = DefaultRouter()
router.register(r"cars", CarViewSet)
router.register(r"rentals", RentalViewSet)
router.register(r"invoices", InvoiceViewSet)

urlpatterns = router.urls