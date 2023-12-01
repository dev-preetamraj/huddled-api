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
    DEFAULT_PROFILE_URL = ('https://res.cloudinary.com/dxgl4eyhq/image/upload/v1701036989/huddled/images/defaults'
                           '/profile_ioi9ke.jpg')
    DEFAULT_COVER_URL = ('https://res.cloudinary.com/dxgl4eyhq/image/upload/v1701037044/huddled/images/defaults'
                         '/cover_x202x0.png')

    email = models.EmailField(max_length=100, unique=True)
    middle_name = models.CharField(max_length=50, null=True, blank=True)
    profile_picture = models.CharField(max_length=500, default=DEFAULT_PROFILE_URL)
    cover_picture = models.CharField(max_length=500, default=DEFAULT_COVER_URL)
    bio = models.CharField(max_length=150, null=True, blank=True)
    mobile_number = models.CharField(max_length=10, null=True, blank=True)
    gender = models.CharField(max_length=6, choices=GENDER_CHOICES, null=True, blank=True)
    relationship_status = models.CharField(max_length=11, choices=RELATIONSHIP_CHOICES, null=True, blank=True)
    street = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    postal_code = models.CharField(max_length=10, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]