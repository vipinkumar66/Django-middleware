from django.contrib import admin
from .models import NewStats
import json
from django.core.serializers.json import DjangoJSONEncoder

@admin.register(NewStats)
class NewStatAdmin(admin.ModelAdmin):
    """
    Customization for the NewStats model in the Django admin panel.
    """

    def changelist_view(self, request, extra_context=None):
        """
        Overrides the changelist_view method to include statistical data.

        Args:
            request (HttpRequest): The HTTP request object.
            extra_context (dict, optional): Additional context data to be included.

        Returns:
            HttpResponse: The HTTP response for rendering the change list view.
        """

        # Retrieve statistical data from the NewStats model
        stat_data = NewStats.objects.annotate().values("win", "mac", "iph", "android", "oth")

        # Serialize the statistical data to JSON
        as_json = json.dumps(list(stat_data), cls=DjangoJSONEncoder)

        # Add the JSON data to the extra context
        extra_context = extra_context or {"stat_data": as_json}

        # Call the parent class's changelist_view method with the modified context
        return super().changelist_view(request, extra_context=extra_context)
