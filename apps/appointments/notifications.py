import logging

from django.conf import settings
from django.core.mail import send_mail

logger = logging.getLogger(__name__)


def _send(subject, body, recipients):
    recipients = [r for r in recipients if r]
    if not recipients:
        return
    try:
        send_mail(subject, body, settings.DEFAULT_FROM_EMAIL, recipients)
    except Exception:
        # Email fail hone par bhi booking ka kaam rukna nahi chahiye
        logger.exception('Email bhejne me dikkat aayi')


def _when(appt):
    return f'{appt.date:%d %b %Y}, {appt.time:%I:%M %p}'


def _doctor_email(appt):
    user = appt.doctor.user
    return user.email if user else None


def booking_created(appt):
    _send(
        'Appointment request mil gayi',
        f'Namaste {appt.patient.first_name},\n\n'
        f'{appt.doctor.name} ke saath aapki appointment request {_when(appt)} ke liye mil gayi hai.\n'
        f'Doctor confirm karenge to aapko email milega.\n\nDoctor Finder',
        [appt.patient.email],
    )
    _send(
        'Nayi appointment request',
        f'Namaste {appt.doctor.name},\n\n'
        f'{appt.patient.first_name} ne {_when(appt)} ke liye appointment maangi hai.\n'
        f'Doctor Panel me jaakar Confirm ya Cancel karein.\n\nDoctor Finder',
        [_doctor_email(appt)],
    )


def status_changed(appt):
    """Doctor ke Confirm/Cancel par patient ko."""
    _send(
        f'Appointment {appt.status}',
        f'Namaste {appt.patient.first_name},\n\n'
        f'{appt.doctor.name} ke saath aapki appointment ({_when(appt)}) ab {appt.status} hai.\n\n'
        f'Doctor Finder',
        [appt.patient.email],
    )


def cancelled_by_patient(appt):
    _send(
        'Appointment cancel ho gayi',
        f'Namaste {appt.doctor.name},\n\n'
        f'{appt.patient.first_name} ne {_when(appt)} wali appointment cancel kar di hai.\n\n'
        f'Doctor Finder',
        [_doctor_email(appt)],
    )


def rescheduled(appt):
    _send(
        'Appointment ka time badla',
        f'Namaste {appt.doctor.name},\n\n'
        f'{appt.patient.first_name} ne appointment ka naya time {_when(appt)} manga hai.\n'
        f'Doctor Panel me dobara Confirm karein.\n\nDoctor Finder',
        [_doctor_email(appt)],
    )