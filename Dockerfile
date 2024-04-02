# Use the Python base image
FROM python:3.12.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set the working directory in the container
WORKDIR /code

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install Gunicorn
RUN pip install gunicorn

# Copy the rest of the application code into the container
COPY . /code/

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Run Gunicorn when the container starts
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "src.main.wsgi:application"]