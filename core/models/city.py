"""
City Model
----------
Represents a city/location, mapped to OpenWeatherMap's city IDs, with geolocation and country code.
"""

from django.db import models

class City(models.Model):
    """
    Stores city/location data for weather lookups.
    Fields:
        openweather_id: Unique OpenWeatherMap city ID
        name: City name
        country_code: ISO 2-letter country code
        lat: Latitude (decimal)
        lon: Longitude (decimal)
    """
    openweather_id = models.PositiveIntegerField(unique=True)
    name           = models.CharField(max_length=100)
    country_code   = models.CharField(max_length=2)
    lat            = models.DecimalField(max_digits=8, decimal_places=5)
    lon            = models.DecimalField(max_digits=8, decimal_places=5)

    class Meta:
        indexes = [
            models.Index(fields=["name", "country_code"]),
        ]
        verbose_name = "City"
        verbose_name_plural = "Cities"

    def __str__(self):
        """String representation: 'City, CC'"""
        return f"{self.name}, {self.country_code}"
