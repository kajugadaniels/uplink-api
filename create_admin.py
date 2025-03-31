import os
from django.contrib.auth import get_user_model

User = get_user_model()

email = os.getenv('DJANGO_SUPERUSER_EMAIL')
name = os.getenv('DJANGO_SUPERUSER_NAME')
phone_number = os.getenv('DJANGO_SUPERUSER_PHONE_NUMBER')
password = os.getenv('DJANGO_SUPERUSER_PASSWORD')

if not User.objects.filter(email=email).exists():
    print("Creating superuser...")
    User.objects.create_superuser(
        email=email,
        name=name,
        phone_number=phone_number,
        password=password
    )
else:
    print("Superuser already exists.")
