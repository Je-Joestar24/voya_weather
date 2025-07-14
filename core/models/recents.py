from .place_relations import _BaseUserCityRelation, models


class RecentView(_BaseUserCityRelation):
    class Meta(_BaseUserCityRelation.Meta):
        unique_together = ()        # allow duplicates
        indexes = [                 # speed up look-ups
            models.Index(fields=["user", "timestamp"]),
        ]
