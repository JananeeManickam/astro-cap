from django.db import models
from django.contrib.auth.models import User

class AstronomicalEvent(models.Model):
    """
    Model to store astronomical events for specific dates
    """
    date = models.DateField()
    event_description = models.TextField()
    event_type = models.CharField(max_length=100, choices=[
        ('DISCOVERY', 'Scientific Discovery'),
        ('BIRTH', 'Astronomer/Scientist Birth'),
        ('DEATH', 'Astronomer/Scientist Death'),
        ('MISSION', 'Space Mission'),
        ('OBSERVATION', 'Astronomical Observation')
    ])
    year = models.IntegerField()
    
    class Meta:
        ordering = ['-date']
        unique_together = ['date', 'event_description']

    def __str__(self):
        return f"{self.date}: {self.event_description[:50]}"