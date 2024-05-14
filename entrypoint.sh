#!/bin/sh

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Collect static files
echo "Collecting static files..."
python manage.py collectstatic --no-input

# Check if admin user exists
if ! python manage.py shell -c "from django.contrib.auth.models import User; exit(0) if User.objects.filter(username='admin').exists() else exit(1)"; then
    # Create admin user
    echo "Creating admin user..."
    echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell
fi

# Start the Django server
exec "$@"