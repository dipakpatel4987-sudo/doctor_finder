import uuid

from django.conf import settings
from django.contrib import messages
from django.http import Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from django.views.decorators.http import require_POST

from apps.appointments.models import Appointment
from apps.core.decorators import patient_required
from .models import Payment


def _my_appointment(request, appt_id):
    return get_object_or_404(Appointment.objects.select_related('doctor'),
                             pk=appt_id, patient=request.user)


@patient_required
def summary(request, appt_id):
    appt = _my_appointment(request, appt_id)
    if appt.status == 'Cancelled':
        messages.error(request, 'Cancelled appointment ka payment nahi ho sakta.')
        return redirect('appointments:patient_list')
    payment = Payment.for_appointment(appt)
    if payment.status == 'Success':
        return redirect('payments:success', appt_id=appt.pk)
    return render(request, 'payments/summary.html', {'appt': appt, 'payment': payment})


@patient_required
@require_POST
def pay(request, appt_id):
    appt = _my_appointment(request, appt_id)
    payment = Payment.for_appointment(appt)
    if payment.status == 'Success':
        return redirect('payments:success', appt_id=appt.pk)
    if appt.status == 'Cancelled':
        return redirect('appointments:patient_list')
    if settings.PAYMENT_MODE != 'mock':
        raise Http404('Real Paytm gateway abhi configure nahi hai.')
    payment.txn_id = 'TXN' + uuid.uuid4().hex[:12].upper()
    payment.status = 'Pending'
    payment.save()
    return render(request, 'payments/gateway.html', {'appt': appt, 'payment': payment})


@patient_required
@require_POST
def complete(request, appt_id):
    if settings.PAYMENT_MODE != 'mock':
        raise Http404()
    appt = _my_appointment(request, appt_id)
    payment = Payment.for_appointment(appt)
    if payment.status == 'Success':
        return redirect('payments:success', appt_id=appt.pk)
    if request.POST.get('result') == 'success':
        payment.status = 'Success'
        payment.paid_at = timezone.now()
        payment.save()
        return redirect('payments:success', appt_id=appt.pk)
    payment.status = 'Failed'
    payment.save()
    return redirect('payments:failed', appt_id=appt.pk)


@patient_required
def success(request, appt_id):
    appt = _my_appointment(request, appt_id)
    payment = get_object_or_404(Payment, appointment=appt, status='Success')
    return render(request, 'payments/success.html', {'appt': appt, 'payment': payment})


@patient_required
def failed(request, appt_id):
    appt = _my_appointment(request, appt_id)
    payment = get_object_or_404(Payment, appointment=appt)
    return render(request, 'payments/failed.html', {'appt': appt, 'payment': payment})


@patient_required
def history(request):
    payments = Payment.objects.filter(appointment__patient=request.user) \
        .select_related('appointment__doctor')
    return render(request, 'payments/history.html', {'payments': payments})