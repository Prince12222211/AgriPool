# 🚀 Quick Start Guide - AgriPool

## Fastest Way to Get Started

### Option 1: Automatic Setup (Recommended)
```bash
./setup.sh
```

### Option 2: Manual Setup

1. **Create and activate virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate
```

2. **Install dependencies:**
```bash
pip install -r requirements.txt
```

3. **Run migrations:**
```bash
python manage.py migrate
```

4. **Add sample crops (optional but recommended):**
```bash
python add_crops.py
```

5. **Create admin user:**
```bash
python manage.py createsuperuser
```
Follow the prompts to create your admin account.

6. **Run the development server:**
```bash
python manage.py runserver
```

7. **Open your browser:**
Visit: http://127.0.0.1:8000/

## 🎯 First Steps After Setup

1. **Register a new account** at http://127.0.0.1:8000/accounts/register/
2. **Complete your profile** with location details
3. **Add a land parcel** to get started with fertilizer planning
4. **Create a transport request** if you need to transport produce

## 🔑 Admin Panel

Access at: http://127.0.0.1:8000/admin/

Use the superuser credentials you created during setup.

## 📱 Features to Try

### Transport Sharing
- ✅ Create transport requests for your produce
- ✅ Browse requests from other farmers
- ✅ Make or receive transport offers
- ✅ Accept offers and track status

### Fertilizer Planning
- ✅ Add land parcels with soil details
- ✅ Select crops and seasons
- ✅ Get NPK recommendations
- ✅ View cost estimates and yield predictions
- ✅ Get application schedules

## 🛠️ Development Commands

```bash
# Activate virtual environment
source venv/bin/activate

# Run development server
python manage.py runserver

# Create migrations (after model changes)
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run tests (when added)
python manage.py test

# Collect static files (for production)
python manage.py collectstatic
```

## 📊 Sample Data

The setup includes 12 sample crops:
- Kharif crops: Rice, Maize, Cotton, Sugarcane, Tomato, Soybean, Pigeon Pea
- Rabi crops: Wheat, Potato, Onion, Mustard, Chickpea

## 🐛 Troubleshooting

### Port already in use?
```bash
python manage.py runserver 8080
```

### Static files not loading?
```bash
python manage.py collectstatic
```

### Database issues?
```bash
rm db.sqlite3
python manage.py migrate
python add_crops.py
```

## 📧 Need Help?

- Check the main README.md for detailed documentation
- Review the code comments
- Create an issue on GitHub

## 🌟 What's Next?

After getting familiar with the app:
1. Add more crops through admin panel
2. Customize fertilizer calculation logic
3. Add more soil types and parameters
4. Integrate weather APIs
5. Add payment processing
6. Deploy to production

Happy farming! 🌾
