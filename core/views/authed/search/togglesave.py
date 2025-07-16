"""
Search Places View Module
-------------------------
Handles searching for cities, displaying weather data, and saving/unsaving places for authenticated users.
"""

from core.views.authed.util  import login_required, redirect, get_object_or_404, City, SavedPlace

@login_required
def toggle_save_place(request, city_id):
    """
    Add or remove a city from the user's saved places. Redirects to search places view.
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