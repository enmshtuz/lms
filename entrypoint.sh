#!/bin/bash

# Apply database migrations
echo "Applying database migrations..."
python manage.py migrate

# Create admin user if not exists
echo "Creating admin user..."
echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'admin@example.com', 'admin')" | python manage.py shell


# Start the Django server
exec "$@"