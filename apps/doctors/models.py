from django.conf import settings
from django.db import models


class Doctor(models.Model):
    SPECIALTIES = [
        ('Cardiologist', 'Cardiologist'),
        ('Dentist', 'Dentist'),
        ('Neurologist', 'Neurologist'),
        ('Dermatologist', 'Dermatologist'),
        ('Pediatrician', 'Pediatrician'),
        ('Orthopedic', 'Orthopedic'),
    ]
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, null=True, blank=True, on_delete=models.SET_NULL,
        limit_choices_to={'role': 'doctor'}, related_name='doctor_profile',
        help_text='Is doctor ka login account (appointments dikhane ke liye)',
    )
    name = models.CharField(max_length=100)
    specialty = models.CharField(max_length=30, choices=SPECIALTIES)
    city = models.CharField(max_length=50)
    phone = models.CharField(max_length=15, blank=True)
    fee = models.PositiveIntegerField(default=500)
    experience = models.PositiveIntegerField(default=1, help_text='Years')
    rating = models.DecimalField(max_digits=2, decimal_places=1, default=4.5)
    education = models.CharField(max_length=200, blank=True)
    about = models.TextField(blank=True)
    latitude = models.FloatField(null=True, blank=True)
    longitude = models.FloatField(null=True, blank=True)
    photo = models.ImageField(upload_to='doctors/', blank=True)
    is_available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-rating', 'name']

    def __str__(self):
        return f'{self.name} ({self.specialty})'