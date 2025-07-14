from django.db import models

class City(models.Model):
    openweather_id = models.PositiveIntegerField(unique=True)
    name           = models.CharField(max_length=100)
    country_code   = models.CharField(max_length=2)
    lat            = models.DecimalField(max_digits=8, decimal_places=5)
    lon            = models.DecimalField(max_digits=8, decimal_places=5)

    class Meta:
        indexes = [
            models.Index(fields=["name", "country_code"]),
        ]

    def __str__(self):
        return f"{self.name}, {self.country_code}"
