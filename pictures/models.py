from django.db import models

class TelescopeObservation(models.Model):
    telescope = models.CharField(max_length=100)  # e.g., "Hubble", "Webb"
    title = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)
    image_url = models.URLField()
    observation_date = models.DateTimeField()
    target_name = models.CharField(max_length=255, blank=True, null=True)
    observation_type = models.CharField(max_length=50, blank=True, null=True)
    is_current = models.BooleanField(default=False)
    metadata = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.telescope} - {self.title}"
    
    class Meta:
        ordering = ['-observation_date']

class TelescopeStatus(models.Model):
    telescope = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=100)
    current_instrument = models.CharField(max_length=100, blank=True, null=True)
    last_update = models.DateTimeField()
    additional_info = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.telescope} - {self.status}"
    
    class Meta:
        verbose_name_plural = "Telescope Statuses"
        

class Constellation(models.Model):
    name = models.CharField(max_length=100)
    id = models.CharField(max_length=10, primary_key=True)
    full_name = models.CharField(max_length=100)
    
    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['name']