# Use the Python base image
FROM python:3.12.2

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

ENV APP_HOME=/code
WORKDIR $APP_HOME

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends netcat-openbsd \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*


# Copy the rest of the application code into the container
COPY . /code/

# Install dependencies
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt


## Copy entrypoint.sh and make it executable
#COPY ./entrypoint.sh /code/entrypoint.sh
#RUN sed -i 's/\r$//g' $APP_HOME/entrypoint.sh
#RUN chmod +x /code/entrypoint.sh
#
## Run entrypoint.sh
#ENTRYPOINT ["/code/entrypoint.sh"]
