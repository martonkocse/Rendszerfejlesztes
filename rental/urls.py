from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),

    path("api/auth/register/", views.register_view, name="register"),
    path("api/auth/login/", views.login_view, name="login"),
    path("api/auth/logout/", views.logout_view, name="logout"),
    path("api/auth/me/", views.me_view, name="me"),

    path("api/protected/customer/", views.customer_only_view, name="customer_only"),
    path("api/protected/agent/", views.agent_only_view, name="agent_only"),
    path("api/protected/admin/", views.admin_only_view, name="admin_only"),
    path("api/protected/staff/", views.staff_only_view, name="staff_only"),
]