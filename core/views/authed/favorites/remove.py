from core.views.authed.util import login_required, FavoritePlace, City, logging, messages, login_required, DatabaseError, get_object_or_404, redirect

logger = logging.getLogger(__name__)

@login_required
def remove_favorite(request, city_id):
    """
    Remove a city from the user's favorites. Handles missing records gracefully.
    Args:
        request (HttpRequest): The HTTP request object.
        city_id (int): The ID of the city to remove from favorites.
    Returns:
        HttpResponse: Redirects to the favorites page with a status message.
    """
    user = request.user
    city = get_object_or_404(City, id=city_id)

    try:
        # .filter().delete() avoids the extra get_or_create() round-trip
        deleted, _ = FavoritePlace.objects.filter(user=user, city=city).delete()
        if deleted:
            messages.info(request, f"✖ {city.name} removed from favorite places.")
        else:
            # No row found; not an error, but useful to know.
            logger.warning("Unsave called but no record for user %s / city %s", user.id, city.id)
            messages.warning(request, f"{city.name} wasn’t in your favorite places.")
    except DatabaseError as e:
        logger.error("Unsave failed for user %s / city %s: %s", user.id, city.id, e)
        messages.error(request, "Couldn’t remove the place—please try again.")

    return redirect("favorite_places_view")