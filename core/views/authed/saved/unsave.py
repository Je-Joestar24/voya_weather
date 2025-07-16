"""
Unsave Place View Module
------------------------
Handles removing a city from the user's saved places via POST request.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from core.views.authed.util import SavedPlace, City, messages, DatabaseError, get_object_or_404, redirect
import logging

logger = logging.getLogger(__name__)

class UnsavePlaceView(LoginRequiredMixin, View):
    """
    Remove a city from the user's saved places. Handles missing records gracefully.
    Only handles POST requests.
    """
    def post(self, request, city_id):
        """
        Remove a city from the user's saved places.
        Args:
            request (HttpRequest): The HTTP request object.
            city_id (int): The ID of the city to remove from saved places.
        Returns:
            HttpResponse: Redirects to the saved places page with a status message.
        """
        user = request.user
        city = get_object_or_404(City, id=city_id)
        try:
            deleted, _ = SavedPlace.objects.filter(user=user, city=city).delete()
            if deleted:
                messages.info(request, f"✖ {city.name} removed from saved places.")
            else:
                logger.warning("Unsave called but no record for user %s / city %s", user.id, city.id)
                messages.warning(request, f"{city.name} wasn’t in your saved places.")
        except DatabaseError as e:
            logger.error("Unsave failed for user %s / city %s: %s", user.id, city.id, e)
            messages.error(request, "Couldn’t remove the place—please try again.")
        return redirect("saved_places_view")