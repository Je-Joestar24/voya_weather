"""
Toggle Favorite Place View Module
--------------------------------
Handles adding or removing a city from the user's favorites via POST request.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from core.views.authed.util import FavoritePlace, City, messages, DatabaseError, IntegrityError, get_object_or_404, redirect
import logging

logger = logging.getLogger(__name__)

class ToggleFavoritePlaceView(LoginRequiredMixin, View):
    """
    Add or remove a city from the user's favorites. Redirects to saved places view.
    Only handles POST requests.
    """
    def post(self, request, city_id):
        """
        Toggle favorite status for a city for the current user.
        Args:
            request (HttpRequest): The HTTP request object.
            city_id (int): The ID of the city to toggle as favorite.
        Returns:
            HttpResponse: Redirects to the saved places page with a status message.
        """
        user = request.user
        city = get_object_or_404(City, id=city_id)
        try:
            favorite, created = FavoritePlace.objects.get_or_create(user=user, city=city)
            if created:
                messages.success(request, f"✔ {city.name} added to favorites.")
            else:
                favorite.delete()
                messages.info(request, f"✖ {city.name} removed from favorites.")
        except (IntegrityError, DatabaseError) as e:
            logger.error("Favorite toggle failed for user %s / city %s: %s", user.id, city.id, e)
            messages.error(request, "Something went wrong—please try again.")
        return redirect("saved_places_view")