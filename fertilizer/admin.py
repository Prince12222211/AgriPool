from django.contrib import admin
from .models import LandParcel, Crop, FertilizerPlan

@admin.register(LandParcel)
class LandParcelAdmin(admin.ModelAdmin):
    list_display = ['parcel_name', 'farmer', 'area', 'soil_type', 'village', 'district', 'state']
    search_fields = ['parcel_name', 'farmer__username', 'village', 'district']
    list_filter = ['soil_type', 'state', 'district']

@admin.register(Crop)
class CropAdmin(admin.ModelAdmin):
    list_display = ['name', 'season', 'duration_days']
    search_fields = ['name']
    list_filter = ['season']

@admin.register(FertilizerPlan)
class FertilizerPlanAdmin(admin.ModelAdmin):
    list_display = ['land_parcel', 'crop', 'season', 'year', 'estimated_yield', 'estimated_fertilizer_cost', 'created_at']
    search_fields = ['land_parcel__parcel_name', 'crop__name', 'land_parcel__farmer__username']
    list_filter = ['season', 'year', 'crop', 'created_at']
