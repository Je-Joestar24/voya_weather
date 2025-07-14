from django.db import models
from django.utils import timezone
from .user import User
from .city import City


class _BaseUserCityRelation(models.Model):
    """
    Abstract: one user ↔ one city + timestamp
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="%(class)ss")
    city = models.ForeignKey(City, on_delete=models.CASCADE, related_name="%(class)ss")
    timestamp = models.DateTimeField(default=timezone.now)

    class Meta:
        abstract = True
        ordering = ["-timestamp"]
        unique_together = ("user", "city")      # prevents duplicates unless you override

    def __str__(self):
        return f"{self.user} ↔ {self.city}"