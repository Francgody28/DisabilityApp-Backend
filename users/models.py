from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class DisabledPerson(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    first_name = models.CharField(max_length=100)
    middle_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.IntegerField()
    gender = models.CharField(max_length=10)
    disability_type = models.CharField(max_length=100)
    contact = models.CharField(max_length=100)

class Location(models.Model):
    full_name = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    latitude = models.FloatField(default=0.0)
    longitude = models.FloatField(default=0.0)


    def __str__(self):
        return self.full_name

    def __str__(self):
        return f"{self.first_name} {self.last_name}"