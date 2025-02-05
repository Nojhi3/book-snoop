import os
import django
from django.contrib.auth import get_user_model

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "book_store.settings")
django.setup()

User = get_user_model()

admin_username = os.getenv("ADMIN_USERNAME", "admin")
admin_email = os.getenv("ADMIN_EMAIL", "admin@example.com")
admin_password = os.getenv("ADMIN_PASSWORD", "admin123")

if not User.objects.filter(username=admin_username).exists():
    print("Creating admin user...")
    User.objects.create_superuser(admin_username, admin_email, admin_password)
    print("Superuser created.")
else:
    print("Admin user already exists. Skipping creation.")
