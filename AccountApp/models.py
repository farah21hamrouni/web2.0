
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinLengthValidator, RegexValidator
from django.core.exceptions import ValidationError
from django.utils import timezone


# User
class User(AbstractUser):
    pass


# Doctor
class Doctor(User):

    license_number = models.CharField(
        max_length=6,
        unique=True,
        validators=[MinLengthValidator(6)]
    )

    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    specialties = models.ManyToManyField('Specialty')

    def __str__(self):
        return f"Dr. {self.first_name} {self.last_name}"


# Patient
class Patient(User):

    national_id = models.CharField(
        max_length=8,
        unique=True,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    phone = models.CharField(
        max_length=8,
        validators=[RegexValidator(r'^\d{8}$')]
    )

    birth_date = models.DateField()

    def clean(self):
        super().clean()

        if self.birth_date and self.birth_date >= timezone.localdate():
            raise ValidationError({
                'birth_date': "La date de naissance doit être antérieure à aujourd'hui."
            })

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


# Specialty
class Specialty(models.Model):

    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name
