"""
FavoritePlace Model
-------------------
Represents a city that a user has marked as a favorite.
"""

from .place_relations import _BaseUserCityRelation

class FavoritePlace(_BaseUserCityRelation):
    """
    User marked a city as favourite.
    Inherits user, city, and timestamp fields from _BaseUserCityRelation.
    """
