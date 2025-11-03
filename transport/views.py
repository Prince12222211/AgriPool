from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from datetime import date
from .models import TransportRequest, TransportOffer, TransportMatch
from accounts.decorators import transporter_required

@login_required
def transport_list(request):
    """List all open transport requests and available offers"""
    requests = TransportRequest.objects.filter(status='open').order_by('-created_at')
    offers = TransportOffer.objects.filter(status='available').order_by('-created_at')
    
    context = {
        'requests': requests,
        'offers': offers,
        'is_transporter': hasattr(request.user, 'transporter_profile')
    }
    return render(request, 'transport/transport_list.html', context)

@login_required
def my_transport_requests(request):
    """List user's transport requests"""
    requests = TransportRequest.objects.filter(farmer=request.user).order_by('-created_at')
    return render(request, 'transport/my_requests.html', {'requests': requests})

@login_required
def create_transport_request(request):
    """Create a new transport request"""
    if request.method == 'POST':
        transport_request = TransportRequest(
            farmer=request.user,
            crop_type=request.POST.get('crop_type'),
            quantity=request.POST.get('quantity'),
            pickup_location=request.POST.get('pickup_location'),
            pickup_village=request.POST.get('pickup_village'),
            pickup_district=request.POST.get('pickup_district'),
            destination_market=request.POST.get('destination_market'),
            destination_district=request.POST.get('destination_district'),
            preferred_date=request.POST.get('preferred_date'),
            flexible_dates=request.POST.get('flexible_dates') == 'on',
            description=request.POST.get('description', ''),
        )
        transport_request.save()
        messages.success(request, 'Transport request created successfully.')
        return redirect('transport:my_transport_requests')
    return render(request, 'transport/create_request.html')

@login_required
@transporter_required
def create_transport_offer(request):
    """Create a new transport offer"""
    if request.method == 'POST':
        transport_offer = TransportOffer(
            transporter=request.user,
            vehicle_type=request.POST.get('vehicle_type'),
            capacity=request.POST.get('capacity'),
            rate_per_km=request.POST.get('rate_per_km'),
            minimum_charge=request.POST.get('minimum_charge'),
            available_from=request.POST.get('available_from'),
            available_to=request.POST.get('available_to'),
            current_location=request.POST.get('current_location'),
            current_district=request.POST.get('current_district'),
            preferred_routes=request.POST.get('preferred_routes'),
            refrigerated=request.POST.get('refrigerated') == 'on',
            vehicle_number=request.POST.get('vehicle_number'),
            driver_name=request.POST.get('driver_name'),
            driver_phone=request.POST.get('driver_phone'),
            insurance_valid_till=request.POST.get('insurance_valid_till'),
        )
        transport_offer.save()
        messages.success(request, 'Transport offer created successfully.')
        return redirect('transport:my_transport_offers')
    return render(request, 'transport/create_offer.html')

@login_required
@transporter_required
def my_transport_offers(request):
    """List transporter's transport offers"""
    offers = TransportOffer.objects.filter(transporter=request.user).order_by('-created_at')
    return render(request, 'transport/my_offers.html', {'offers': offers})

@login_required
def transport_detail(request, request_id):
    """View transport request details and matching offers"""
    transport_request = get_object_or_404(TransportRequest, id=request_id)
    matched_offers = TransportOffer.objects.filter(
        status='available',
        available_from__lte=transport_request.preferred_date,
        available_to__gte=transport_request.preferred_date,
        capacity__gte=transport_request.quantity / 10  # Convert quintals to tons
    ).order_by('rate_per_km')
    
    context = {
        'transport_request': transport_request,
        'matched_offers': matched_offers,
        'existing_matches': transport_request.matches.all()
    }
    return render(request, 'transport/transport_detail.html', context)

@login_required
@transporter_required
def create_transport_match(request, request_id):
    """Create a match between transport request and offer"""
    transport_request = get_object_or_404(TransportRequest, id=request_id)
    if request.method == 'POST':
        offer_id = request.POST.get('offer_id')
        transport_offer = get_object_or_404(TransportOffer, id=offer_id, transporter=request.user)
        
        # Calculate costs
        estimated_distance = float(request.POST.get('estimated_distance', 0))
        rate_per_km = float(transport_offer.rate_per_km)
        total_cost = max(
            transport_offer.minimum_charge,
            estimated_distance * rate_per_km
        )
        
        match = TransportMatch(
            transport_request=transport_request,
            transport_offer=transport_offer,
            proposed_rate=rate_per_km,
            estimated_distance=estimated_distance,
            total_cost=total_cost
        )
        match.save()
        
        messages.success(request, 'Transport match created successfully.')
        return redirect('transport:transport_detail', request_id=request_id)
    return redirect('transport:transport_list')

@login_required
def accept_transport_match(request, match_id):
    """Accept a transport match"""
    match = get_object_or_404(TransportMatch, id=match_id)
    if request.user == match.transport_request.farmer:
        match.status = 'accepted'
        match.save()
        
        # Update related request and offer
        match.transport_request.status = 'in_progress'
        match.transport_request.save()
        match.transport_offer.status = 'assigned'
        match.transport_offer.save()
        
        messages.success(request, 'Transport match accepted successfully.')
    return redirect('transport:transport_detail', request_id=match.transport_request.id)

@login_required
def complete_transport(request, match_id):
    """Mark transport as completed and add ratings"""
    match = get_object_or_404(TransportMatch, id=match_id)
    if request.method == 'POST':
        if request.user == match.transport_request.farmer:
            match.transporter_rating = request.POST.get('rating')
            match.transporter_review = request.POST.get('review')
        elif request.user == match.transport_offer.transporter:
            match.farmer_rating = request.POST.get('rating')
            match.farmer_review = request.POST.get('review')
        
        match.status = 'completed'
        match.save()
        
        # Update related request and offer
        match.transport_request.status = 'completed'
        match.transport_request.save()
        match.transport_offer.status = 'available'
        match.transport_offer.save()
        
        messages.success(request, 'Transport marked as completed.')
        return redirect('transport:transport_detail', request_id=match.transport_request.id)
    
    return render(request, 'transport/complete_transport.html', {'match': match})
