#!/bin/bash

echo "🌾 AgriPool Setup Script 🌾"
echo "============================"
echo ""

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "✅ Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Run migrations
echo "🗄️  Running database migrations..."
python manage.py makemigrations
python manage.py migrate

# Create necessary directories
echo "📁 Creating necessary directories..."
mkdir -p media/profile_pics media/crops

echo ""
echo "✅ Setup complete!"
echo ""
echo "📝 Next steps:"
echo "1. Activate virtual environment: source venv/bin/activate"
echo "2. Create superuser: python manage.py createsuperuser"
echo "3. Run server: python manage.py runserver"
echo "4. Visit: http://127.0.0.1:8000/"
echo ""
echo "Happy farming! 🚜"
