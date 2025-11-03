from django.db import models
from django.contrib.auth.models import User

class FarmerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='farmer_profile')
    phone_number = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    village = models.CharField(max_length=100, blank=True)
    district = models.CharField(max_length=100, blank=True)
    state = models.CharField(max_length=100, blank=True)
    pin_code = models.CharField(max_length=10, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Farmer Profile"

    class Meta:
        verbose_name = 'Farmer Profile'
        verbose_name_plural = 'Farmer Profiles'


class TransporterProfile(models.Model):
    TRANSPORTER_TYPES = [
        ('individual', 'Individual'),
        ('company', 'Company'),
        ('cooperative', 'Cooperative'),
    ]

    LICENSE_TYPES = [
        ('national', 'National Permit'),
        ('state', 'State Permit'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='transporter_profile')
    transporter_type = models.CharField(max_length=20, choices=TRANSPORTER_TYPES)
    company_name = models.CharField(max_length=200, blank=True)
    registration_number = models.CharField(max_length=50, blank=True)
    gst_number = models.CharField(max_length=15, blank=True)
    license_type = models.CharField(max_length=20, choices=LICENSE_TYPES)
    license_number = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=15)
    alternate_phone = models.CharField(max_length=15, blank=True)
    office_address = models.TextField()
    district = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    pin_code = models.CharField(max_length=10)
    profile_picture = models.ImageField(upload_to='profile_pics/', blank=True, null=True)
    fleet_size = models.PositiveIntegerField(default=1)
    years_of_experience = models.PositiveIntegerField()
    insurance_provider = models.CharField(max_length=100)
    insurance_policy_number = models.CharField(max_length=50)
    insurance_valid_till = models.DateField()
    average_rating = models.DecimalField(max_digits=3, decimal_places=2, default=0.0)
    total_ratings = models.PositiveIntegerField(default=0)
    verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Transporter Profile"

    class Meta:
        verbose_name = 'Transporter Profile'
        verbose_name_plural = 'Transporter Profiles'


class UserDocument(models.Model):
    DOCUMENT_TYPES = [
        ('id_proof', 'ID Proof'),
        ('address_proof', 'Address Proof'),
        ('license', 'License'),
        ('registration', 'Registration Certificate'),
        ('insurance', 'Insurance Policy'),
        ('permit', 'Transport Permit'),
        ('other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='documents')
    document_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES)
    document_number = models.CharField(max_length=50)
    document_file = models.FileField(upload_to='user_documents/')
    valid_till = models.DateField(null=True, blank=True)
    verified = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    verified_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_document_type_display()}"
