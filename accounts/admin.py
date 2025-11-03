from django.contrib import admin
from .models import FarmerProfile

@admin.register(FarmerProfile)
class FarmerProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'village', 'district', 'state', 'phone_number', 'created_at']
    search_fields = ['user__username', 'village', 'district', 'state']
    list_filter = ['state', 'district', 'created_at']
