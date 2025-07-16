"""
RecentView Model
----------------
Tracks cities recently viewed by a user. Allows duplicates and is indexed for fast look-up by user and timestamp.
"""

from .place_relations import _BaseUserCityRelation, models


class RecentView(_BaseUserCityRelation):
    """
    User recently viewed a city.
    Allows duplicates (multiple views of the same city).
    Inherits user, city, and timestamp fields from _BaseUserCityRelation.
    """
    class Meta(_BaseUserCityRelation.Meta):
        unique_together = ()        # allow duplicates
        indexes = [                 # speed up look-ups
            models.Index(fields=["user", "timestamp"]),
        ]
