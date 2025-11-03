from django.db import models
from django.contrib.auth.models import User

class LandParcel(models.Model):
    SOIL_TYPES = [
        ('alluvial', 'Alluvial'),
        ('black', 'Black'),
        ('red', 'Red'),
        ('laterite', 'Laterite'),
        ('desert', 'Desert'),
        ('mountain', 'Mountain'),
    ]

    IRRIGATION_TYPES = [
        ('irrigated', 'Irrigated'),
        ('rainfed', 'Rainfed'),
    ]
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='land_parcels')
    parcel_name = models.CharField(max_length=100)
    area = models.DecimalField(max_digits=10, decimal_places=2, help_text="Area in acres")
    soil_type = models.CharField(max_length=20, choices=SOIL_TYPES)
    location = models.CharField(max_length=200)
    village = models.CharField(max_length=100)
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    latitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, null=True, blank=True)
    soil_ph = models.DecimalField(max_digits=4, decimal_places=2, null=True, blank=True)
    organic_carbon = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Percentage")
    nitrogen_level = models.CharField(max_length=20, blank=True, help_text="Low/Medium/High")
    phosphorus_level = models.CharField(max_length=20, blank=True, help_text="Low/Medium/High")
    potassium_level = models.CharField(max_length=20, blank=True, help_text="Low/Medium/High")
    irrigation_type = models.CharField(max_length=20, choices=IRRIGATION_TYPES, blank=True)
    rainfall_mm = models.DecimalField(max_digits=6, decimal_places=1, null=True, blank=True, help_text="Annual rainfall (mm)")
    soil_ec = models.DecimalField(max_digits=5, decimal_places=2, null=True, blank=True, help_text="Soil electrical conductivity (dS/m)")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.parcel_name} - {self.farmer.username}"


class Crop(models.Model):
    SEASON_CHOICES = [
        ('kharif', 'Kharif (Monsoon)'),
        ('rabi', 'Rabi (Winter)'),
        ('zaid', 'Zaid (Summer)'),
    ]
    
    WATER_REQUIREMENT = [
        ('low', 'Low (300-500mm)'),
        ('medium', 'Medium (500-700mm)'),
        ('high', 'High (>700mm)'),
    ]
    
    name = models.CharField(max_length=100)
    scientific_name = models.CharField(max_length=100, blank=True)
    season = models.CharField(max_length=20, choices=SEASON_CHOICES)
    duration_days = models.IntegerField(help_text="Average crop duration in days", default=120)
    min_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text="Minimum temperature (°C)", default=15.0)
    max_temperature = models.DecimalField(max_digits=4, decimal_places=1, help_text="Maximum temperature (°C)", default=35.0)
    rainfall_requirement = models.CharField(max_length=10, choices=WATER_REQUIREMENT, default='medium')
    soil_ph_min = models.DecimalField(max_digits=3, decimal_places=1, default=6.0)
    soil_ph_max = models.DecimalField(max_digits=3, decimal_places=1, default=7.5)
    nitrogen_requirement = models.DecimalField(max_digits=6, decimal_places=2, help_text="kg/acre", default=50.0)
    phosphorus_requirement = models.DecimalField(max_digits=6, decimal_places=2, help_text="kg/acre", default=25.0)
    potassium_requirement = models.DecimalField(max_digits=6, decimal_places=2, help_text="kg/acre", default=25.0)
    suitable_soil_types = models.CharField(max_length=200, help_text="Comma-separated list of suitable soil types", default="alluvial,black")
    expected_yield = models.DecimalField(max_digits=6, decimal_places=2, help_text="Average yield in quintals/acre", default=20.0)
    market_price = models.DecimalField(max_digits=8, decimal_places=2, help_text="Average market price (Rs/quintal)", default=2000.0)
    description = models.TextField(blank=True)
    planting_method = models.TextField(blank=True)
    irrigation_schedule = models.TextField(blank=True)
    pest_diseases = models.TextField(blank=True, help_text="Common pests and diseases")
    storage_info = models.TextField(blank=True, help_text="Storage requirements and shelf life")
    image = models.ImageField(upload_to='crops/', blank=True, null=True)

    def __str__(self):
        return self.name


class FertilizerPlan(models.Model):
    land_parcel = models.ForeignKey(LandParcel, on_delete=models.CASCADE, related_name='fertilizer_plans')
    crop = models.ForeignKey(Crop, on_delete=models.CASCADE)
    season = models.CharField(max_length=20)
    year = models.IntegerField()
    
    # NPK Recommendations (kg per parcel)
    nitrogen_kg = models.DecimalField(max_digits=8, decimal_places=2)
    phosphorus_kg = models.DecimalField(max_digits=8, decimal_places=2)
    potassium_kg = models.DecimalField(max_digits=8, decimal_places=2)
    
    # Organic recommendations
    organic_manure_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    compost_kg = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    
    # Micronutrients
    zinc_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    boron_kg = models.DecimalField(max_digits=6, decimal_places=2, default=0)
    
    # Cost and yield
    estimated_fertilizer_cost = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_yield = models.DecimalField(max_digits=10, decimal_places=2, help_text="Expected yield in quintals (parcel total)")
    estimated_revenue = models.DecimalField(max_digits=10, decimal_places=2)
    target_yield = models.DecimalField(max_digits=6, decimal_places=2, null=True, blank=True, help_text="Target yield per acre (quintals)")
    
    application_schedule = models.TextField(help_text="Timeline for fertilizer application")
    additional_notes = models.TextField(blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop.name} Plan for {self.land_parcel.parcel_name} - {self.season} {self.year}"

    class Meta:
        ordering = ['-created_at']
