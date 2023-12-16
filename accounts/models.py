import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class CustomUser(AbstractUser):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )

    RELATIONSHIP_CHOICES = (
        ('Single', 'Single'),
        ('Married', 'Married'),
        ('Divorced', 'Divorced'),
        ('Complicated', 'Complicated')
    )
    DEFAULT_COVER_URL = ('https://res.cloudinary.com/dxgl4eyhq/image/upload/v1701037044/huddled/images/defaults'
                         '/cover_x202x0.png')

    id = models.CharField(primary_key=True, unique=True, max_length=100, default=f'huddled_user_{uuid.uuid4()}')
    email = models.EmailField(max_length=100, unique=True)
    username = models.CharField(max_length=100, unique=True, default=f'huddled_{uuid.uuid4()}')
    cover_picture = models.CharField(max_length=500, default=DEFAULT_COVER_URL)
    bio = models.CharField(max_length=150, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    relationship_status = models.CharField(max_length=11, choices=RELATIONSHIP_CHOICES, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]
