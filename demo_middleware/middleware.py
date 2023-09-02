from django.db.models import F
from .models import NewStats

class DemoMiddleWware:
    """
    Custom middleware for updating statistics based on user's operating system.

    This middleware checks the user's operating system in the User-Agent header
    of the HTTP request and updates statistics in the NewStats model accordingly.
    """

    def __init__(self, get_response):
        """
        Initialize the middleware.

        Args:
            get_response (callable): The next middleware or view function in the stack.
        """
        self.get_response = get_response

    def stats(self, os_data):
        """
        Update statistics based on the user's operating system.

        Args:
            os_data (str): The user's operating system data from the User-Agent header.
        """
        # Check the user's operating system and update the corresponding statistic field
        if "Windows" in os_data:
            NewStats.objects.all().update(win=F('win')+1)
        elif "mac" in os_data:
            NewStats.objects.all().update(mac=F('mac')+1)
        elif "iPhone" in os_data:
            NewStats.objects.all().update(iph=F('iph')+1)
        elif "Android" in os_data:
            NewStats.objects.all().update(android=F('android')+1)
        else:
            NewStats.objects.all().update(oth=F('oth')+1)

    def __call__(self, request):
        """
        Process the incoming HTTP request.

        This method is called for each incoming HTTP request and performs the
        middleware's logic to update statistics.

        Args:
            request (HttpRequest): The incoming HTTP request object.

        Returns:
            HttpResponse: The HTTP response object.
        """
        # Extract the User-Agent header from the request to determine the user's device
        device = request.META["HTTP_USER_AGENT"]

        # Check if the request path contains "admin" to exclude admin panel requests
        if "admin" not in request.path:
            # Update statistics based on the user's operating system
            self.stats(device)

        # Call the next middleware or view function and return its response
        response = self.get_response(request)
        return response
