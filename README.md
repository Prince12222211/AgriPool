# AgriPool - Smart Agriculture Platform

AgriPool is a comprehensive web application built with Django that provides two key services for farmers:

## Features

### 1. **Transport Sharing**
- Post agricultural produce transport requirements
- Browse available transport requests from other farmers
- Connect with transporters and receive competitive offers
- Pool transportation costs to reduce expenses
- Track transport request status (Open, In Progress, Completed)

### 2. **Fertilizer Planning**
- Add and manage land parcels with soil characteristics
- Get customized fertilizer recommendations based on:
  - Soil type and pH
  - NPK (Nitrogen, Phosphorus, Potassium) levels
  - Crop selection and season
  - Land area
- View estimated costs and expected yields
- Get detailed application schedules
- Maximize returns with precision agriculture

## Technology Stack

- **Backend**: Django 4.2
- **Frontend**: Bootstrap 5, HTML5, CSS3, JavaScript
- **Database**: SQLite (development)
- **Icons**: Font Awesome 6
- **Fonts**: Google Fonts (Poppins)

## Project Structure

```
AgriPool/
├── accounts/          # User authentication and profiles
├── transport/         # Transport sharing module
├── fertilizer/        # Fertilizer planning module
├── agripool/          # Main project settings
├── templates/         # HTML templates
├── static/           # CSS, JS, images
├── media/            # User uploads
└── manage.py
```

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python3 manage.py makemigrations
python3 manage.py migrate
```

### 3. Create Superuser (Admin)

```bash
python3 manage.py createsuperuser
```

### 4. Add Sample Crops (Optional)

```bash
python3 manage.py shell
```

Then in the shell:
```python
from fertilizer.models import Crop

crops_data = [
    {"name": "Wheat", "season": "rabi", "duration_days": 120},
    {"name": "Rice", "season": "kharif", "duration_days": 150},
    {"name": "Maize", "season": "kharif", "duration_days": 90},
    {"name": "Cotton", "season": "kharif", "duration_days": 180},
    {"name": "Sugarcane", "season": "kharif", "duration_days": 365},
    {"name": "Potato", "season": "rabi", "duration_days": 90},
    {"name": "Tomato", "season": "kharif", "duration_days": 75},
]

for crop_data in crops_data:
    Crop.objects.get_or_create(**crop_data)

exit()
```

### 5. Run Development Server

```bash
python3 manage.py runserver
```

Visit http://127.0.0.1:8000/ in your browser.

## Usage Guide

### For Farmers

1. **Register** - Create your account
2. **Complete Profile** - Add your location and contact details
3. **Transport Module**:
   - Post transport requests for your produce
   - Browse other farmers' requests
   - Receive and accept offers from transporters
4. **Fertilizer Module**:
   - Add your land parcels with soil details
   - Create fertilizer plans for specific crops
   - View recommendations and cost estimates

### For Transporters

1. **Register** - Create your account
2. **Browse Requests** - View open transport requests
3. **Make Offers** - Submit competitive price offers
4. **Track Status** - Monitor accepted offers

## Admin Panel

Access the admin panel at http://127.0.0.1:8000/admin/

Features:
- Manage users and profiles
- View all transport requests and offers
- Manage land parcels and fertilizer plans
- Add/edit crop database

## API Endpoints

### Accounts
- `/` - Homepage
- `/accounts/register/` - User registration
- `/accounts/login/` - User login
- `/accounts/dashboard/` - User dashboard
- `/accounts/profile/` - User profile

### Transport
- `/transport/` - Browse transport requests
- `/transport/create/` - Create new request
- `/transport/my-requests/` - View your requests
- `/transport/<id>/` - Request details
- `/transport/<id>/offer/` - Make an offer

### Fertilizer
- `/fertilizer/` - View land parcels
- `/fertilizer/create/` - Add land parcel
- `/fertilizer/<id>/` - Parcel details
- `/fertilizer/<id>/plan/create/` - Create fertilizer plan

## Database Models

### Accounts
- `FarmerProfile` - Extended user profile with location details

### Transport
- `TransportRequest` - Transport requirements posted by farmers
- `TransportOffer` - Offers made by transporters

### Fertilizer
- `LandParcel` - Farm land with soil characteristics
- `Crop` - Crop database with season and duration
- `FertilizerPlan` - Customized fertilizer recommendations

## Future Enhancements

- Real-time notifications
- Payment gateway integration
- Weather API integration
- Crop disease detection
- Market price integration
- Mobile app (React Native/Flutter)
- Multi-language support
- GPS tracking for transport
- Analytics dashboard

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License.

## Support

For support, email info@agripool.com or create an issue in the repository.

## Screenshots

(Add screenshots here after deployment)

---

**Built with ❤️ for farmers**
# AgriPool
