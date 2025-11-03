from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class TransportRequest(models.Model):
    STATUS_CHOICES = [
        ('open', 'Open'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    farmer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_requests')
    crop_type = models.CharField(max_length=100)
    quantity = models.DecimalField(max_digits=10, decimal_places=2, help_text="Quantity in quintals")
    pickup_location = models.CharField(max_length=200)
    pickup_village = models.CharField(max_length=100)
    pickup_district = models.CharField(max_length=100)
    destination_market = models.CharField(max_length=200)
    destination_district = models.CharField(max_length=100)
    preferred_date = models.DateField()
    flexible_dates = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='open')
    description = models.TextField(blank=True)
    estimated_cost = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.crop_type} - {self.farmer.username} ({self.pickup_village} to {self.destination_market})"

class TransportOffer(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('assigned', 'Assigned'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]

    VEHICLE_TYPES = [
        ('mini_truck', 'Mini Truck (1-3 tons)'),
        ('small_truck', 'Small Truck (3-7 tons)'),
        ('medium_truck', 'Medium Truck (7-12 tons)'),
        ('large_truck', 'Large Truck (12+ tons)'),
        ('refrigerated', 'Refrigerated Truck'),
    ]
    
    transporter = models.ForeignKey(User, on_delete=models.CASCADE, related_name='transport_offers')
    vehicle_type = models.CharField(max_length=20, choices=VEHICLE_TYPES)
    capacity = models.DecimalField(max_digits=5, decimal_places=1, help_text="Capacity in tons", default=5.0)
    rate_per_km = models.DecimalField(max_digits=6, decimal_places=2, help_text="Rate per kilometer in Rs.", default=25.0)
    minimum_charge = models.DecimalField(max_digits=8, decimal_places=2, help_text="Minimum charge in Rs.", default=1000.0)
    available_from = models.DateField(default=timezone.now)
    available_to = models.DateField(null=True, blank=True)
    current_location = models.CharField(max_length=200, default="New Delhi")
    current_district = models.CharField(max_length=100, default="New Delhi")
    preferred_routes = models.TextField(blank=True, help_text="Comma-separated list of preferred districts")
    refrigerated = models.BooleanField(default=False)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='available')
    vehicle_number = models.CharField(max_length=20, default="DL01XX0000")
    driver_name = models.CharField(max_length=100, default="Driver Name")
    driver_phone = models.CharField(max_length=15, default="9999999999")
    insurance_valid_till = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.vehicle_type} - {self.transporter.username} ({self.current_district})"

class TransportMatch(models.Model):
    STATUS_CHOICES = [
        ('proposed', 'Proposed'),
        ('accepted', 'Accepted'),
        ('rejected', 'Rejected'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    ]
    
    transport_request = models.ForeignKey(TransportRequest, on_delete=models.CASCADE, related_name='matches')
    transport_offer = models.ForeignKey(TransportOffer, on_delete=models.CASCADE, related_name='matches')
    proposed_rate = models.DecimalField(max_digits=10, decimal_places=2)
    estimated_distance = models.DecimalField(max_digits=6, decimal_places=1, help_text="Distance in kilometers")
    total_cost = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='proposed')
    farmer_rating = models.IntegerField(null=True, blank=True)
    farmer_review = models.TextField(blank=True)
    transporter_rating = models.IntegerField(null=True, blank=True)
    transporter_review = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Match: {self.transport_request} - {self.transport_offer}"

    class Meta:
        ordering = ['-created_at']



