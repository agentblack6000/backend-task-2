from django.urls import path
from django.contrib.auth import views as auth_views

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path(
        "login/",
        auth_views.LoginView.as_view(
            template_name="passengers/login.html", redirect_authenticated_user=True
        ),
        name="passenger-login",
    ),
    path("logout/", auth_views.LogoutView.as_view(), name="passenger-logout"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("dashboard/purchase", views.purchase, name="purchase"),
    path(
        "dashboard/purchase/confirmation/<int:ticket_id>",
        views.confirmation,
        name="confirmation",
    ),
    path("signup/", views.signup, name="signup"),
    path("finances/", views.add_money, name="money"),
]
