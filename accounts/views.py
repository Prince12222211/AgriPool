from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.contrib.auth.models import User
from .models import FarmerProfile, TransporterProfile, UserDocument
from transport.models import TransportRequest, TransportOffer, TransportMatch
from fertilizer.models import LandParcel, Crop
from datetime import date
from django.db.models import Avg, Count

def home(request):
    """Homepage view"""
    return render(request, 'home.html')

def register(request):
    """User registration view with role selection"""
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            role = request.POST.get('role')
            
            if role == 'farmer':
                FarmerProfile.objects.create(user=user)
                messages.success(request, f'Farmer account created for {user.username}! Please complete your profile.')
            elif role == 'transporter':
                TransporterProfile.objects.create(
                    user=user,
                    transporter_type='individual',
                    license_type='state',
                    years_of_experience=0
                )
                messages.success(request, f'Transporter account created for {user.username}! Please complete your profile.')
            
            login(request, user)
            return redirect('accounts:profile')
    else:
        form = UserCreationForm()
    return render(request, 'accounts/register.html', {'form': form, 'roles': ['farmer', 'transporter']})

@login_required
def profile(request):
    """User profile view and edit"""
    if request.method == 'POST':
        if hasattr(request.user, 'farmer_profile'):
            profile = request.user.farmer_profile
            profile.phone_number = request.POST.get('phone_number')
            profile.address = request.POST.get('address')
            profile.village = request.POST.get('village')
            profile.district = request.POST.get('district')
            profile.state = request.POST.get('state')
            profile.pin_code = request.POST.get('pin_code')
            if request.FILES.get('profile_picture'):
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
        elif hasattr(request.user, 'transporter_profile'):
            profile = request.user.transporter_profile
            profile.transporter_type = request.POST.get('transporter_type')
            profile.company_name = request.POST.get('company_name')
            profile.registration_number = request.POST.get('registration_number')
            profile.gst_number = request.POST.get('gst_number')
            profile.license_type = request.POST.get('license_type')
            profile.license_number = request.POST.get('license_number')
            profile.phone_number = request.POST.get('phone_number')
            profile.alternate_phone = request.POST.get('alternate_phone')
            profile.office_address = request.POST.get('office_address')
            profile.district = request.POST.get('district')
            profile.state = request.POST.get('state')
            profile.pin_code = request.POST.get('pin_code')
            profile.fleet_size = request.POST.get('fleet_size')
            profile.years_of_experience = request.POST.get('years_of_experience')
            profile.insurance_provider = request.POST.get('insurance_provider')
            profile.insurance_policy_number = request.POST.get('insurance_policy_number')
            profile.insurance_valid_till = request.POST.get('insurance_valid_till')
            if request.FILES.get('profile_picture'):
                profile.profile_picture = request.FILES['profile_picture']
            profile.save()
        
        messages.success(request, 'Profile updated successfully.')
        return redirect('accounts:dashboard')
    
    # Get the appropriate profile
    if hasattr(request.user, 'farmer_profile'):
        profile = request.user.farmer_profile
    elif hasattr(request.user, 'transporter_profile'):
        profile = request.user.transporter_profile
    else:
        profile = None

    return render(request, 'accounts/profile.html', {'profile': profile})

@login_required
def dashboard(request):
    """User dashboard with role-specific information"""
    context = {
        'user': request.user,
    }
    
    if hasattr(request.user, 'farmer_profile'):
        # Farmer dashboard
        context.update({
            'role': 'farmer',
            'land_parcels': LandParcel.objects.filter(farmer=request.user),
            'transport_requests': TransportRequest.objects.filter(farmer=request.user),
            'active_matches': TransportMatch.objects.filter(
                transport_request__farmer=request.user,
                status__in=['proposed', 'accepted']
            ),
            'recent_crops': Crop.objects.filter(land_parcel__farmer=request.user).distinct()[:5],
        })
    elif hasattr(request.user, 'transporter_profile'):
        # Transporter dashboard
        active_offers = TransportOffer.objects.filter(
            transporter=request.user,
            status__in=['available', 'assigned']
        )
        context.update({
            'role': 'transporter',
            'transport_offers': active_offers,
            'active_matches': TransportMatch.objects.filter(
                transport_offer__transporter=request.user,
                status__in=['proposed', 'accepted']
            ),
            'rating': request.user.transporter_profile.average_rating,
            'total_trips': TransportMatch.objects.filter(
                transport_offer__transporter=request.user,
                status='completed'
            ).count(),
        })
    
    return render(request, 'accounts/dashboard.html', context)

@login_required
def upload_document(request):
    """Handle document uploads for user verification"""
    if request.method == 'POST':
        document = UserDocument(
            user=request.user,
            document_type=request.POST.get('document_type'),
            document_number=request.POST.get('document_number'),
            document_file=request.FILES['document_file'],
            valid_till=request.POST.get('valid_till')
        )
        document.save()
        messages.success(request, 'Document uploaded successfully. It will be verified soon.')
        return redirect('accounts:profile')
    return render(request, 'accounts/upload_document.html')

def user_login(request):
    """User login view"""
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f'Welcome back, {username}!')
                next_url = request.POST.get('next') or request.GET.get('next')
                if next_url:
                    return redirect(next_url)
                return redirect('accounts:dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def user_logout(request):
    """User logout view"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('accounts:home')


