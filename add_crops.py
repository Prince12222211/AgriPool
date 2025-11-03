#!/usr/bin/env python
"""
Script to add sample crops to the database
Run with: python manage.py shell < add_crops.py
Or: ./venv/bin/python manage.py shell < add_crops.py
"""

import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'agripool.settings')
django.setup()

from fertilizer.models import Crop

crops_data = [
    {"name": "Wheat", "season": "rabi", "duration_days": 120, "description": "Major cereal crop grown in winter season"},
    {"name": "Rice", "season": "kharif", "duration_days": 150, "description": "Staple food crop grown during monsoon"},
    {"name": "Maize", "season": "kharif", "duration_days": 90, "description": "Versatile cereal crop for food and feed"},
    {"name": "Cotton", "season": "kharif", "duration_days": 180, "description": "Major fiber crop"},
    {"name": "Sugarcane", "season": "kharif", "duration_days": 365, "description": "Long duration cash crop"},
    {"name": "Potato", "season": "rabi", "duration_days": 90, "description": "Important tuber crop"},
    {"name": "Tomato", "season": "kharif", "duration_days": 75, "description": "Popular vegetable crop"},
    {"name": "Onion", "season": "rabi", "duration_days": 120, "description": "Essential vegetable crop"},
    {"name": "Soybean", "season": "kharif", "duration_days": 100, "description": "Important oilseed and protein crop"},
    {"name": "Mustard", "season": "rabi", "duration_days": 90, "description": "Major oilseed crop of rabi season"},
    {"name": "Chickpea", "season": "rabi", "duration_days": 120, "description": "Important pulse crop"},
    {"name": "Pigeon Pea", "season": "kharif", "duration_days": 150, "description": "Long duration pulse crop"},
]

print("Adding sample crops to database...")
print("=" * 50)

created_count = 0
existing_count = 0

for crop_data in crops_data:
    crop, created = Crop.objects.get_or_create(
        name=crop_data['name'],
        defaults={
            'season': crop_data['season'],
            'duration_days': crop_data['duration_days'],
            'description': crop_data.get('description', '')
        }
    )
    
    if created:
        print(f"✅ Created: {crop.name} ({crop.season})")
        created_count += 1
    else:
        print(f"⏭️  Already exists: {crop.name}")
        existing_count += 1

print("=" * 50)
print(f"\n📊 Summary:")
print(f"  - New crops created: {created_count}")
print(f"  - Existing crops: {existing_count}")
print(f"  - Total crops in database: {Crop.objects.count()}")
print("\n✅ Done!")
