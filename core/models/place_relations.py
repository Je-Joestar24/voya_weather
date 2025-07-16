"""
User-City Relationship Base Model
---------------------------------
Defines an abstract base model for relationships between users and cities (e.g., saved, favorite, recent), including timestamp.
"""

from django.db import models
from django.utils import timezone
from .user import User
from .city import City


class _BaseUserCityRelation(models.Model):
    """
    Abstract base model for user-city relationships.
    Fields:
        user: ForeignKey to User
        city: ForeignKey to City
        timestamp: When the relation was created
    Meta:
        abstract: Not a database table
        ordering: Most recent first
        unique_together: (user, city) unless overridden
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)ss")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="%(class)ss")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ["-timestamp"]
        unique_together = ("user", "city")      # prevents duplicates unless you override

    def __str__(self):
        """String representation: 'user ↔ city'"""
        return f"{self.user} ↔ {self.city}"