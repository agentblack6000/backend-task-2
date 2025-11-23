from django.urls import path
from . import views

app_name = "scanner"

urlpatterns = [
    path("", views.index, name="index"),
    path("offline", views.purchase_offline, name="offline")
]