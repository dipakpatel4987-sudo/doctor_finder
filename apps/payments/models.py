from decimal import Decimal

from django.db import models

from apps.appointments.models import Appointment

GST_RATE = Decimal('0.18')


class Payment(models.Model):
    STATUS = [('Pending', 'Pending'), ('Success', 'Success'), ('Failed', 'Failed')]

    appointment = models.OneToOneField(Appointment, on_delete=models.CASCADE, related_name='payment')
    amount = models.DecimalField(max_digits=8, decimal_places=2)
    gst = models.DecimalField(max_digits=8, decimal_places=2)
    total = models.DecimalField(max_digits=8, decimal_places=2)
    status = models.CharField(max_length=10, choices=STATUS, default='Pending')
    txn_id = models.CharField(max_length=40, blank=True)
    paid_at = models.DateTimeField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    @classmethod
    def for_appointment(cls, appt):
        """Is appointment ka payment record deta hai, nahi hai to banata hai."""
        amount = Decimal(appt.doctor.fee)
        gst = (amount * GST_RATE).quantize(Decimal('0.01'))
        obj, _ = cls.objects.get_or_create(
            appointment=appt,
            defaults={'amount': amount, 'gst': gst, 'total': amount + gst},
        )
        return obj

    def __str__(self):
        return f'{self.appointment} - Rs.{self.total} [{self.status}]'