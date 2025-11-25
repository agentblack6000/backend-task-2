"""
Handles improper login/logout
"""
from django.contrib.auth import logout
from django.shortcuts import redirect
from django.core.exceptions import ObjectDoesNotExist


class LogoutOnMissingPassengerMiddleware:
    """
    Logs out users if a related object (like a passenger) is missing,
    then redirects them to the login page.
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # This runs before the view
        response = self.get_response(request)
        return response

    # Called when a view raises an exception
    def process_exception(self, request, exception):
        if isinstance(exception, ObjectDoesNotExist):
            logout(request)
            return redirect("passenger-login")
        return None
