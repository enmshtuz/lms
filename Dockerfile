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
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy entrypoint.sh and make it executable
COPY ./entrypoint.sh /lms/entrypoint.sh
RUN chmod +x /lms/entrypoint.sh

# Run entrypoint.sh
ENTRYPOINT ["/lms/entrypoint.sh"]
