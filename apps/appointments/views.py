from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.core.decorators import patient_required, doctor_required
from apps.doctors.models import Doctor
from . import notifications
from .forms import BookingForm, RescheduleForm, ReviewForm
from .models import Appointment


@patient_required
def book(request):
    initial = {}
    doc_id = request.GET.get('doctor')
    if doc_id and Doctor.objects.filter(pk=doc_id, is_available=True).exists():
        initial['doctor'] = doc_id

    form = BookingForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        appt = form.save(commit=False)
        appt.patient = request.user
        appt.save()
        notifications.booking_created(appt)
        messages.success(request, 'Appointment request bhej di gayi. Ab payment karein.')
        return redirect('payments:summary', appt_id=appt.pk)
    return render(request, 'appointments/book.html', {'form': form})


@patient_required
def patient_list(request):
    appts = Appointment.objects.filter(patient=request.user).select_related('doctor')
    return render(request, 'appointments/patient_list.html', {'appointments': appts})


@patient_required
@require_POST
def patient_cancel(request, pk):
    appt = get_object_or_404(Appointment, pk=pk, patient=request.user)
    if appt.status in ('Pending', 'Confirmed'):
        appt.status = 'Cancelled'
        appt.save()
        notifications.cancelled_by_patient(appt)
        messages.success(request, 'Appointment cancel ho gayi.')
    return redirect('appointments:patient_list')


@patient_required
def patient_reschedule(request, pk):
    appt = get_object_or_404(Appointment.objects.select_related('doctor'), pk=pk, patient=request.user)
    if appt.status == 'Cancelled':
        messages.error(request, 'Cancelled appointment reschedule nahi ho sakti.')
        return redirect('appointments:patient_list')
    form = RescheduleForm(request.POST or None, instance=appt)
    if request.method == 'POST' and form.is_valid():
        appt = form.save(commit=False)
        appt.status = 'Pending'
        appt.save()
        notifications.rescheduled(appt)
        messages.success(request, 'Naya time bhej diya gaya. Doctor dobara confirm karega.')
        return redirect('appointments:patient_list')
    return render(request, 'appointments/reschedule.html', {'form': form, 'appt': appt})


@doctor_required
def doctor_list(request):
    profile = getattr(request.user, 'doctor_profile', None)
    appts = Appointment.objects.none()
    if profile:
        appts = Appointment.objects.filter(doctor=profile).select_related('patient')
        status = request.GET.get('status', '')
        if status in ('Pending', 'Confirmed', 'Cancelled'):
            appts = appts.filter(status=status)
    return render(request, 'appointments/doctor_list.html', {
        'appointments': appts, 'profile': profile,
        'status': request.GET.get('status', ''),
    })


@doctor_required
@require_POST
def doctor_update(request, pk, action):
    profile = getattr(request.user, 'doctor_profile', None)
    appt = get_object_or_404(Appointment, pk=pk, doctor=profile) if profile else None
    if appt is None:
        return redirect('appointments:doctor_list')
    if action == 'confirm' and appt.status == 'Pending':
        appt.status = 'Confirmed'
    elif action == 'cancel' and appt.status in ('Pending', 'Confirmed'):
        appt.status = 'Cancelled'
    else:
        return redirect('appointments:doctor_list')
    appt.save()
    notifications.status_changed(appt)
    messages.success(request, f'Appointment {appt.status} ho gayi.')
    return redirect('appointments:doctor_list')
@patient_required
def review_create(request, pk):
    appt = get_object_or_404(Appointment.objects.select_related('doctor'), pk=pk, patient=request.user)
    if not appt.can_review:
        messages.error(request, 'Is appointment ka review abhi nahi diya ja sakta.')
        return redirect('appointments:patient_list')
    form = ReviewForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        review = form.save(commit=False)
        review.appointment = appt
        review.patient = request.user
        review.doctor = appt.doctor
        review.save()
        messages.success(request, 'Review dene ke liye shukriya!')
        return redirect('appointments:patient_list')
    return render(request, 'appointments/review.html', {'form': form, 'appt': appt})