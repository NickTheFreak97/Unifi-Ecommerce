from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    id = models.CharField(max_length=36, primary_key=True)
    phoneNumber = models.CharField(max_length=15, null=True)
    streetAddress = models.CharField(max_length=127, null=True)
    zipCode = models.CharField(max_length=10, null=True)
    municipality = models.CharField(max_length=255, null=True)
    countryCode = models.CharField(max_length=2, null=True)
    sessionID = models.CharField(max_length=63)
    isVerified = models.BooleanField(default=False)