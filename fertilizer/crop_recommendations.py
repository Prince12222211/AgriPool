from typing import List, Dict, Any
from .models import LandParcel, Crop
from datetime import date

def get_seasonal_temperature(month: int) -> Dict[str, float]:
    """Returns typical temperature ranges for different months"""
    # Simplified temperature data for Indian agriculture zones
    temp_data = {
        # Winter (Dec-Feb)
        12: {'min': 10, 'max': 25},
        1: {'min': 8, 'max': 23},
        2: {'min': 12, 'max': 26},
        # Spring (Mar-May)
        3: {'min': 15, 'max': 30},
        4: {'min': 20, 'max': 35},
        5: {'min': 25, 'max': 40},
        # Monsoon (Jun-Sep)
        6: {'min': 25, 'max': 35},
        7: {'min': 24, 'max': 33},
        8: {'min': 24, 'max': 32},
        9: {'min': 23, 'max': 31},
        # Autumn (Oct-Nov)
        10: {'min': 18, 'max': 30},
        11: {'min': 14, 'max': 28},
    }
    return temp_data.get(month, {'min': 20, 'max': 30})

def calculate_crop_suitability_score(crop: Crop, parcel: LandParcel, season: str, month: int) -> float:
    """
    Calculate a suitability score (0-1) for a crop based on land parcel conditions
    """
    score = 1.0
    temp_data = get_seasonal_temperature(month)
    
    # Check soil type suitability
    suitable_soils = [s.strip().lower() for s in crop.suitable_soil_types.split(',')]
    if parcel.soil_type not in suitable_soils:
        score *= 0.5
    
    # Check pH suitability
    if parcel.soil_ph:
        if not (crop.soil_ph_min <= parcel.soil_ph <= crop.soil_ph_max):
            ph_diff = min(abs(parcel.soil_ph - crop.soil_ph_min), 
                         abs(parcel.soil_ph - crop.soil_ph_max))
            score *= max(0.3, 1 - ph_diff * 0.2)
    
    # Check temperature suitability
    if not (crop.min_temperature <= temp_data['max'] <= crop.max_temperature):
        temp_diff = min(abs(temp_data['max'] - crop.min_temperature),
                       abs(temp_data['max'] - crop.max_temperature))
        score *= max(0.3, 1 - temp_diff * 0.1)
    
    # Check water availability
    if parcel.irrigation_type == 'rainfed' and crop.rainfall_requirement == 'high':
        score *= 0.4
    elif parcel.irrigation_type == 'irrigated':
        score *= 1.0
    elif parcel.rainfall_mm:
        if crop.rainfall_requirement == 'high' and parcel.rainfall_mm < 700:
            score *= 0.5
        elif crop.rainfall_requirement == 'medium' and parcel.rainfall_mm < 500:
            score *= 0.7
    
    # Season match
    if crop.season != season:
        score *= 0.2
    
    return round(score, 2)

def get_crop_recommendations(parcel: LandParcel, season: str = None) -> List[Dict[str, Any]]:
    """
    Get crop recommendations for a land parcel based on soil conditions and season
    """
    if not season:
        # Determine season based on current month
        month = date.today().month
        if month in [6, 7, 8, 9]:
            season = 'kharif'
        elif month in [10, 11, 12, 1, 2]:
            season = 'rabi'
        else:
            season = 'zaid'
    
    all_crops = Crop.objects.all()
    recommendations = []
    
    for crop in all_crops:
        suitability_score = calculate_crop_suitability_score(crop, parcel, season, date.today().month)
        
        if suitability_score > 0.3:  # Only include somewhat suitable crops
            estimated_yield = round(crop.expected_yield * suitability_score, 2)
            estimated_revenue = round(estimated_yield * float(parcel.area) * float(crop.market_price), 2)
            
            recommendations.append({
                'crop': crop,
                'suitability_score': suitability_score,
                'estimated_yield_per_acre': estimated_yield,
                'total_estimated_yield': round(estimated_yield * float(parcel.area), 2),
                'estimated_revenue': estimated_revenue,
                'season': season,
                'growing_duration': crop.duration_days,
                'water_requirement': crop.get_rainfall_requirement_display(),
                'key_requirements': [
                    f"Soil pH: {crop.soil_ph_min}-{crop.soil_ph_max}",
                    f"Temperature: {crop.min_temperature}°C-{crop.max_temperature}°C",
                    f"Growing period: {crop.duration_days} days",
                ],
                'cultivation_tips': crop.planting_method,
                'market_price': crop.market_price,
            })
    
    # Sort by suitability score and estimated revenue
    recommendations.sort(key=lambda x: (x['suitability_score'], x['estimated_revenue']), reverse=True)
    
    return recommendations