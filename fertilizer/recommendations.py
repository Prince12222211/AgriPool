from typing import Dict, Any
from decimal import Decimal

def get_npk_requirements(crop_type: str, season: str) -> Dict[str, float]:
    """
    Returns base NPK requirements per acre for different crops and seasons.
    Values are approximate and should be adjusted based on local conditions.
    """
    requirements = {
        'rice': {
            'kharif': {'N': 100, 'P': 50, 'K': 50},
            'rabi': {'N': 120, 'P': 60, 'K': 60}
        },
        'wheat': {
            'rabi': {'N': 120, 'P': 60, 'K': 40}
        },
        'maize': {
            'kharif': {'N': 120, 'P': 60, 'K': 40},
            'rabi': {'N': 150, 'P': 75, 'K': 50}
        },
        'cotton': {
            'kharif': {'N': 100, 'P': 50, 'K': 50}
        },
        'sugarcane': {
            'zaid': {'N': 150, 'P': 85, 'K': 85}
        }
    }
    
    default_values = {'N': 80, 'P': 40, 'K': 40}
    return requirements.get(crop_type, {}).get(season, default_values)

def adjust_for_soil_type(base_values: Dict[str, float], soil_type: str) -> Dict[str, float]:
    """
    Adjusts NPK requirements based on soil type
    """
    adjustments = {
        'alluvial': {'N': 1.0, 'P': 1.0, 'K': 1.0},
        'black': {'N': 0.8, 'P': 1.2, 'K': 0.9},
        'red': {'N': 1.2, 'P': 1.1, 'K': 0.9},
        'laterite': {'N': 1.3, 'P': 1.2, 'K': 1.1},
        'desert': {'N': 1.4, 'P': 1.0, 'K': 1.2},
        'mountain': {'N': 1.1, 'P': 1.1, 'K': 1.0}
    }
    
    factors = adjustments.get(soil_type, {'N': 1.0, 'P': 1.0, 'K': 1.0})
    return {
        'N': base_values['N'] * factors['N'],
        'P': base_values['P'] * factors['P'],
        'K': base_values['K'] * factors['K']
    }

def compute_recommendations(parcel, crop, season: str, target_yield_per_acre: float | None) -> Dict[str, Any]:
    area = float(getattr(parcel, 'area', 1) or 1)
    soil_type = getattr(parcel, 'soil_type', 'alluvial')
    soil_ph = float(getattr(parcel, 'soil_ph', 7.0) or 7.0)
    organic_carbon = float(getattr(parcel, 'organic_carbon', 0.5) or 0.5)
    
    # Get base NPK requirements
    base_npk = get_npk_requirements(crop.name.lower(), season)
    
    # Adjust for soil type
    adjusted_npk = adjust_for_soil_type(base_npk, soil_type)
    
    # Adjust for pH
    ph_factor = 1.0
    if soil_ph < 6.5:
        ph_factor = 1.2  # Increase for acidic soils
    elif soil_ph > 7.5:
        ph_factor = 1.1  # Slight increase for alkaline soils
    
    # Adjust for organic carbon content
    organic_factor = 1.0
    if organic_carbon < 0.5:
        organic_factor = 1.2
    elif organic_carbon > 1.0:
        organic_factor = 0.8

    # Apply yield target scaling
    scale = 1.0
    if target_yield_per_acre and target_yield_per_acre > 0:
        scale = min(2.0, max(0.5, target_yield_per_acre / 20.0))
    
    # Calculate final recommendations
    n_total = round(adjusted_npk['N'] * area * scale * ph_factor * organic_factor, 2)
    p_total = round(adjusted_npk['P'] * area * scale * ph_factor, 2)
    k_total = round(adjusted_npk['K'] * area * scale * ph_factor, 2)

    # Calculate organic matter and micronutrients
    organic_total = round(2000.0 * area * (1.2 if organic_carbon < 0.5 else 1.0), 2)
    compost_total = round(1000.0 * area * (1.2 if organic_carbon < 0.5 else 1.0), 2)
    
    # Micronutrients based on soil type and pH
    zinc_total = round(25.0 * area * (1.2 if soil_ph > 7.5 else 1.0), 2)
    boron_total = round(5.0 * area * (1.2 if soil_ph < 6.5 else 1.0), 2)
    
    # Calculate costs (approximate market rates in Rs.)
    urea_qty = round(n_total * 2.17, 2)  # Convert N to Urea (46% N)
    dap_qty = round(p_total * 2.17, 2)   # Convert P to DAP (46% P)
    mop_qty = round(k_total * 1.67, 2)   # Convert K to MOP (60% K)
    
    cost = {
        'urea': round(urea_qty * 12, 2),      # Rs. 12 per kg
        'dap': round(dap_qty * 24, 2),        # Rs. 24 per kg
        'mop': round(mop_qty * 18, 2),        # Rs. 18 per kg
        'organic': round(organic_total * 2, 2),  # Rs. 2 per kg
        'compost': round(compost_total * 3, 2),  # Rs. 3 per kg
        'zinc': round(zinc_total * 50, 2),      # Rs. 50 per kg
        'boron': round(boron_total * 80, 2),    # Rs. 80 per kg
    }
    
    return {
        'npk': {
            'N': n_total,
            'P': p_total,
            'K': k_total,
        },
        'fertilizers': {
            'urea': urea_qty,
            'dap': dap_qty,
            'mop': mop_qty,
            'organic': organic_total,
            'compost': compost_total,
            'zinc_sulphate': zinc_total,
            'borax': boron_total,
        },
        'costs': cost,
        'total_cost': round(sum(cost.values()), 2),
        'application_schedule': generate_application_schedule(season),
    }

def generate_application_schedule(season: str) -> Dict[str, str]:
    """
    Generates a schedule for fertilizer application based on the crop season.
    Returns a dictionary with timing and instructions for each fertilizer type.
    """
    if season == 'kharif':
        return {
            'basal_dose': 'Apply before sowing (June):' + 
                '\n- 1/3rd of Nitrogen (Urea)' +
                '\n- Full dose of Phosphorus (DAP)' +
                '\n- Full dose of Potash (MOP)' +
                '\n- Full dose of Zinc and Boron' +
                '\n- Full dose of organic fertilizers',
            'first_top_dress': 'Apply 30 days after sowing (July):' +
                '\n- 1/3rd of Nitrogen (Urea)',
            'second_top_dress': 'Apply 60 days after sowing (August):' +
                '\n- Remaining 1/3rd of Nitrogen (Urea)'
        }
    elif season == 'rabi':
        return {
            'basal_dose': 'Apply before sowing (November):' +
                '\n- 1/2 of Nitrogen (Urea)' +
                '\n- Full dose of Phosphorus (DAP)' +
                '\n- Full dose of Potash (MOP)' +
                '\n- Full dose of Zinc and Boron' +
                '\n- Full dose of organic fertilizers',
            'first_top_dress': 'Apply with first irrigation (December):' +
                '\n- 1/4th of Nitrogen (Urea)',
            'second_top_dress': 'Apply with second irrigation (January):' +
                '\n- Remaining 1/4th of Nitrogen (Urea)'
        }
    else:  # zaid season
        return {
            'basal_dose': 'Apply before sowing (March):' +
                '\n- 1/2 of Nitrogen (Urea)' +
                '\n- Full dose of Phosphorus (DAP)' +
                '\n- Full dose of Potash (MOP)' +
                '\n- Full dose of Zinc and Boron' +
                '\n- Full dose of organic fertilizers',
            'first_top_dress': 'Apply 30 days after sowing (April):' +
                '\n- Remaining 1/2 of Nitrogen (Urea)'
        }

    # Dummy costing: Rs per kg
    cost = (
        n_total * 25 +
        p_total * 30 +
        k_total * 28 +
        organic_total * 2 +
        compost_total * 3 +
        zinc_total * 150 +
        boron_total * 200
    )

    # Dummy yield/revenue estimates
    est_yield_quintals_total = round((target_yield_per_acre or 20.0) * area * 1.05, 2)
    est_revenue = round(est_yield_quintals_total * 2500, 2)

    application_schedule = [
        {
            "stage": "Basal",
            "timing": "At planting",
            "details": f"Apply {n_total*0.5:.2f} kg N, {p_total*0.7:.2f} kg P2O5, {k_total*0.5:.2f} kg K2O per parcel",
        },
        {
            "stage": "Topdress",
            "timing": "30-35 days after sowing",
            "details": f"Apply {n_total*0.3:.2f} kg N and {k_total*0.3:.2f} kg K2O per parcel",
        },
        {
            "stage": "Flowering",
            "timing": "55-60 days after sowing",
            "details": f"Apply {n_total*0.2:.2f} kg N and {k_total*0.2:.2f} kg K2O per parcel",
        },
    ]

    return {
        'nitrogen_total_kg': n_total,
        'phosphorus_total_kg': p_total,
        'potassium_total_kg': k_total,
        'organic_manure_total_kg': organic_total,
        'compost_total_kg': compost_total,
        'zinc_total_kg': zinc_total,
        'boron_total_kg': boron_total,
        'estimated_cost_rs': round(cost, 2),
        'estimated_yield_quintals_total': est_yield_quintals_total,
        'estimated_revenue_rs': est_revenue,
        'application_schedule': application_schedule,
    }
