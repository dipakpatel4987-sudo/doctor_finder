from datetime import date, timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor, Availability

User = get_user_model()


def next_monday():
    d = date.today() + timedelta(days=1)
    while d.weekday() != 0:
        d += timedelta(days=1)
    return d


class BookingTests(TestCase):
    def setUp(self):
        self.patient = User.objects.create_user(
            email='p@test.com', password='Test@12345', first_name='Patient',
            role='patient', is_approved=True)
        self.doctor = Doctor.objects.create(name='Dr. Test', specialty='Dentist', city='Surat')
        Availability.objects.create(doctor=self.doctor, weekday=0,
                                    start_time='10:00', end_time='13:00')
        self.client.force_login(self.patient)
        self.url = reverse('appointments:book')

    def post(self, d, t):
        return self.client.post(self.url, {
            'doctor': self.doctor.pk, 'date': d.isoformat(), 'time': t, 'reason': ''})

    def test_valid_booking(self):
        self.post(next_monday(), '11:00')
        self.assertEqual(Appointment.objects.count(), 1)

    def test_outside_hours_rejected(self):
        self.post(next_monday(), '15:00')
        self.assertEqual(Appointment.objects.count(), 0)

    def test_wrong_day_rejected(self):
        self.post(next_monday() + timedelta(days=1), '11:00')
        self.assertEqual(Appointment.objects.count(), 0)

    def test_double_booking_rejected(self):
        self.post(next_monday(), '11:00')
        self.post(next_monday(), '11:00')
        self.assertEqual(Appointment.objects.count(), 1)

    def test_past_date_rejected(self):
        self.post(date.today() - timedelta(days=1), '11:00')
        self.assertEqual(Appointment.objects.count(), 0)


class AccessTests(TestCase):
    def test_patient_cannot_open_doctor_panel(self):
        p = User.objects.create_user(email='p2@test.com', password='Test@12345',
                                     first_name='Pat', role='patient', is_approved=True)
        self.client.force_login(p)
        resp = self.client.get(reverse('appointments:doctor_list'))
        self.assertEqual(resp.status_code, 302)