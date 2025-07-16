from core.views.authed.util import login_required, redirect, get_object_or_404, SavedPlace, City, logging, messages, login_required, DatabaseError, get_object_or_404, redirect

logger = logging.getLogger(__name__)

@login_required
def unsave_place_view(request, city_id):
    """
    Remove a city from the user's saved places. Handles missing records gracefully.
    Args:
        request (HttpRequest): The HTTP request object.
        city_id (int): The ID of the city to remove from saved places.
    Returns:
        HttpResponse: Redirects to the saved places page with a status message.
    """
    user = request.user
    city = get_object_or_404(City, id=city_id)

    try:
        # .filter().delete() avoids the extra get_or_create() round-trip
        deleted, _ = SavedPlace.objects.filter(user=user, city=city).delete()
        if deleted:
            messages.info(request, f"✖ {city.name} removed from saved places.")
        else:
            # No row found; not an error, but useful to know.
            logger.warning("Unsave called but no record for user %s / city %s", user.id, city.id)
            messages.warning(request, f"{city.name} wasn’t in your saved places.")
    except DatabaseError as e:
        logger.error("Unsave failed for user %s / city %s: %s", user.id, city.id, e)
        messages.error(request, "Couldn’t remove the place—please try again.")

    return redirect("saved_places_view")