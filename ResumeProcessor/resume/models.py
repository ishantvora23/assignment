from django.db import models

# Create your models here.

class Candidate(models.Model):
    first_name = models.CharField(max_length=100)  # Candidate's first name
    email = models.EmailField(unique=True)  # Candidate's email
    mobile_number = models.CharField(max_length=10, unique=True)  # Mobile number (CharField for flexibility)

    def __str__(self):
        return self.first_name  