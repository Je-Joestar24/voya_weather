"""
SavedPlace Model
----------------
Represents a city that a user has manually saved.
"""

from .place_relations import _BaseUserCityRelation

class SavedPlace(_BaseUserCityRelation):
    """
    User manually saved a city.
    Inherits user, city, and timestamp fields from _BaseUserCityRelation.
    """