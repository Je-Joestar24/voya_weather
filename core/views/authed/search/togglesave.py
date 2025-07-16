"""
Toggle Save Place View Module
----------------------------
Handles adding or removing a city from the user's saved places via POST request.
"""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from core.views.authed.util  import get_object_or_404, City, SavedPlace, redirect

class ToggleSavePlaceView(LoginRequiredMixin, View):
    """
    Add or remove a city from the user's saved places. Redirects to search places view.
    Only handles POST requests.
    """
    def post(self, request, city_id):
        """
        Toggle save status for a city for the current user.
        Args:
            request (HttpRequest): The HTTP request object.
            city_id (int): The ID of the city to toggle as saved.
        Returns:
            HttpResponse: Redirects to the search places page.
        """
        city = get_object_or_404(City, id=city_id)
        user = request.user
        saved, created = SavedPlace.objects.get_or_create(user=user, city=city)
        if not created:
            # Already saved, so unsave (delete)
            saved.delete()
        return redirect('search_places_view')