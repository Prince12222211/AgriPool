from django.contrib import admin
from .models import TransportRequest, TransportOffer

@admin.register(TransportRequest)
class TransportRequestAdmin(admin.ModelAdmin):
    list_display = ['farmer', 'crop_type', 'quantity', 'pickup_village', 'destination_market', 'status', 'preferred_date', 'created_at']
    search_fields = ['farmer__username', 'crop_type', 'pickup_village', 'destination_market']
    list_filter = ['status', 'pickup_district', 'destination_district', 'created_at']
    date_hierarchy = 'preferred_date'

@admin.register(TransportOffer)
class TransportOfferAdmin(admin.ModelAdmin):
    list_display = ['transporter', 'vehicle_type', 'capacity', 'rate_per_km', 'status', 'current_district', 'created_at']
    search_fields = ['transporter__username', 'vehicle_type', 'current_district', 'vehicle_number']
    list_filter = ['status', 'vehicle_type', 'current_district', 'created_at']
