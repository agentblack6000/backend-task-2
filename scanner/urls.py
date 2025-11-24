from django.urls import path
from . import views

app_name = "scanner"

urlpatterns = [
    path("", views.index, name="index"),
    path("offline", views.purchase_offline, name="offline"),
    path("scanner", views.scan_tickets, name="scanner"),
    path("scanner/incoming", views.incoming, name="scanner-incoming"),
    path("scanner/outgoing", views.outgoing, name="scanner-outgoing"),
]
