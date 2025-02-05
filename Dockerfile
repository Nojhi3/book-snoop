# Use the latest stable Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy project files (first requirements.txt to optimize caching)
COPY requirements.txt .

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt gunicorn

# Copy the rest of the application
COPY . .

# Ensure static files exist
RUN mkdir -p /app/static

# Collect static files
RUN python manage.py collectstatic --noinput || true

# Expose port 8000 for Django
EXPOSE 8000

# Run migrations and start the server
CMD ["sh", "-c", "python manage.py migrate && python manage.py collectstatic --noinput && python scripts/create_admin.py && gunicorn book_store.wsgi:application --bind 0.0.0.0:8000"]
