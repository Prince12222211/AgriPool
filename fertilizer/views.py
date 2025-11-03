from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import LandParcel, Crop, FertilizerPlan
from datetime import datetime
from .recommendations import compute_recommendations
from .crop_recommendations import get_crop_recommendations

@login_required
def land_parcel_list(request):
    """List user's land parcels"""
    parcels = LandParcel.objects.filter(farmer=request.user)
    return render(request, 'fertilizer/land_parcel_list.html', {'parcels': parcels})

@login_required
def create_land_parcel(request):
    """Create a new land parcel"""
    if request.method == 'POST':
        parcel = LandParcel(
            farmer=request.user,
            parcel_name=request.POST.get('parcel_name'),
            area=request.POST.get('area'),
            soil_type=request.POST.get('soil_type'),
            location=request.POST.get('location'),
            village=request.POST.get('village'),
            district=request.POST.get('district'),
            state=request.POST.get('state'),
            soil_ph=request.POST.get('soil_ph') or None,
            organic_carbon=request.POST.get('organic_carbon') or None,
            nitrogen_level=request.POST.get('nitrogen_level', ''),
            phosphorus_level=request.POST.get('phosphorus_level', ''),
            potassium_level=request.POST.get('potassium_level', ''),
            irrigation_type=request.POST.get('irrigation_type', ''),
            rainfall_mm=request.POST.get('rainfall_mm') or None,
            soil_ec=request.POST.get('soil_ec') or None,
        )
        parcel.save()
        messages.success(request, 'Land parcel created successfully.')
        return redirect('fertilizer:land_parcel_list')
    return render(request, 'fertilizer/create_land_parcel.html')

@login_required
def land_parcel_detail(request, parcel_id):
    """View land parcel details"""
    parcel = get_object_or_404(LandParcel, id=parcel_id, farmer=request.user)
    return render(request, 'fertilizer/land_parcel_detail.html', {'parcel': parcel})

@login_required
def crop_recommendations(request, parcel_id):
    """Get crop recommendations for a land parcel"""
    parcel = get_object_or_404(LandParcel, id=parcel_id, farmer=request.user)
    season = request.GET.get('season')
    recommendations = get_crop_recommendations(parcel, season)
    
    context = {
        'land_parcel': parcel,
        'recommendations': recommendations,
        'season': season or 'kharif'  # Default to kharif if no season specified
    }
    return render(request, 'fertilizer/crop_recommendations.html', context)

@login_required
def land_parcel_detail(request, parcel_id):
    """View land parcel details and fertilizer plans"""
    parcel = get_object_or_404(LandParcel, id=parcel_id, farmer=request.user)
    plans = parcel.fertilizer_plans.all().order_by('-created_at')
    
    context = {
        'parcel': parcel,
        'plans': plans,
    }
    return render(request, 'fertilizer/land_parcel_detail.html', context)

@login_required
def create_fertilizer_plan(request, parcel_id):
    """Create a fertilizer plan for a land parcel"""
    parcel = get_object_or_404(LandParcel, id=parcel_id, farmer=request.user)
    crops = Crop.objects.all()
    
    if request.method == 'POST':
        crop = get_object_or_404(Crop, id=request.POST.get('crop'))
        season = request.POST.get('season')
        target_yield_per_acre = request.POST.get('target_yield')
        target_yield_per_acre = float(target_yield_per_acre) if target_yield_per_acre else None

        rec = compute_recommendations(parcel=parcel, crop=crop, season=season, target_yield_per_acre=target_yield_per_acre)

        plan = FertilizerPlan(
            land_parcel=parcel,
            crop=crop,
            season=season,
            year=datetime.now().year,
            nitrogen_kg=rec['nitrogen_total_kg'],
            phosphorus_kg=rec['phosphorus_total_kg'],
            potassium_kg=rec['potassium_total_kg'],
            organic_manure_kg=rec['organic_manure_total_kg'],
            compost_kg=rec['compost_total_kg'],
            zinc_kg=rec['zinc_total_kg'],
            boron_kg=rec['boron_total_kg'],
            estimated_fertilizer_cost=rec['estimated_cost_rs'],
            estimated_yield=rec['estimated_yield_quintals_total'],
            estimated_revenue=rec['estimated_revenue_rs'],
            target_yield=target_yield_per_acre,
            application_schedule=rec['application_schedule'],
            additional_notes=request.POST.get('additional_notes', ''),
        )
        plan.save()
        messages.success(request, 'Fertilizer plan created successfully!')
        return redirect('fertilizer:land_parcel_detail', parcel_id=parcel.id)
    
    context = {
        'parcel': parcel,
        'crops': crops,
    }
    return render(request, 'fertilizer/create_plan.html', context)

@login_required
def fertilizer_plan_detail(request, plan_id):
    """View fertilizer plan details"""
    plan = get_object_or_404(FertilizerPlan, id=plan_id, land_parcel__farmer=request.user)
    return render(request, 'fertilizer/plan_detail.html', {'plan': plan})
