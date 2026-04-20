from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("api/auth/register/", views.register_view, name="register"),
    path("api/auth/login/", views.login_view, name="login"),
    path("api/auth/logout/", views.logout_view, name="logout"),
    path("api/auth/me/", views.me_view, name="me"),

    path("api/cars/", views.car_list_view, name="car_list"),
    path("api/cars/<int:car_id>/availability/", views.car_availability_view, name="car_availability"),

    path("api/rentals/", views.create_rental_view, name="create_rental"),
    path("api/rentals/<int:rental_id>/status/", views.update_rental_status_view, name="update_rental_status"),

    path("api/protected/customer/", views.customer_only_view, name="customer_only"),
    path("api/protected/agent/", views.agent_only_view, name="agent_only"),
    path("api/protected/admin/", views.admin_only_view, name="admin_only"),
    path("api/protected/staff/", views.staff_only_view, name="staff_only"),
]