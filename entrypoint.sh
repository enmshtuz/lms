#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Check if admin user exists
if ! python manage.py shell -c "from django.contrib.auth.models import User; from django.utils import timezone; from src.apps.userAuth.models import EmailVerification, SiteSettings; user=User.objects.create_superuser('admin', 'admin@example.com', 'admin'); EmailVerification.objects.create(user=user, token=None, created_at=timezone.now()); site_settings = SiteSettings.objects.create(); site_settings.save()"; then
    # Create admin user
    echo "Creating admin user..."
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi

# Start the Django server
exec "$@"