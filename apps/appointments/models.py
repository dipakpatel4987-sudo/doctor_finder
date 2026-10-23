from datetime import date

from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

from apps.doctors.models import Doctor


class Appointment(models.Model):
    STATUS = [('Pending', 'Pending'), ('Confirmed', 'Confirmed'), ('Cancelled', 'Cancelled')]

    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='appointments')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='appointments')
    date = models.DateField()
    time = models.TimeField()
    reason = models.TextField(blank=True)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-time']

    @property
    def can_review(self):
        """Confirmed, date nikal chuki, aur abhi review nahi diya."""
        return (self.status == 'Confirmed'
                and self.date <= date.today()
                and not hasattr(self, 'review'))

    def __str__(self):
        return f'{self.patient.first_name} -> {self.doctor.name} ({self.date} {self.time}) [{self.status}]'


class Review(models.Model):
    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='review')
    patient = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                                related_name='reviews')
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE, related_name='reviews')
    rating = models.PositiveSmallIntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)])
    comment = models.TextField(blank=True, max_length=500)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @property
    def stars(self):
        return '★' * self.rating + '☆' * (5 - self.rating)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Doctor ki rating = saare reviews ka average
        avg = self.doctor.reviews.aggregate(a=models.Avg('rating'))['a']
        if avg is not None:
            self.doctor.rating = round(avg, 1)
            self.doctor.save(update_fields=['rating'])

    def __str__(self):
        return f'{self.doctor.name}: {self.rating}/5 by {self.patient.first_name}'