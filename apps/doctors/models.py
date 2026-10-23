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

    def check_slot(self, d, t):
        """Date/time doctor ke schedule me hai? Galat ho to message deta hai, theek ho to None."""
        rows = list(self.availability.all())
        if not rows:
            return None  # schedule set nahi, to koi bhi time chalega
        day_rows = [r for r in rows if r.weekday == d.weekday()]
        if not day_rows:
            return f'{self.name} {d:%A} ko available nahi hain.'
        if not any(r.start_time <= t < r.end_time for r in day_rows):
            return 'Ye time doctor ke available time se bahar hai. Doctor ka schedule dekhein.'
        return None

    def __str__(self):
        return f'{self.name} ({self.specialty})'


class Availability(models.Model):
    DAYS = [(0, 'Monday'), (1, 'Tuesday'), (2, 'Wednesday'), (3, 'Thursday'),
            (4, 'Friday'), (5, 'Saturday'), (6, 'Sunday')]

    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='availability')
    weekday = models.PositiveSmallIntegerField(choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()

    class Meta:
        ordering = ['weekday', 'start_time']
        verbose_name_plural = 'Availability'

    def __str__(self):
        return f'{self.doctor.name}: {self.get_weekday_display()} {self.start_time:%H:%M}-{self.end_time:%H:%M}'