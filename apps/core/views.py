from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import get_user_model
from django.db.models import Count, Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.appointments.models import Appointment
from apps.doctors.models import Doctor
from apps.payments.models import Payment


def home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('accounts:dashboard')
    available = Doctor.objects.filter(is_available=True)
    return render(request, 'core/home.html', {
        'top_doctors': available[:4],
        'doctor_count': available.count(),
    })


@staff_member_required
def admin_dashboard(request):
    User = get_user_model()
    revenue = Payment.objects.filter(status='Success').aggregate(t=Sum('total'))['t'] or 0
    return render(request, 'core/admin_dashboard.html', {
        'patients': User.objects.filter(role='patient').count(),
        'doctors': Doctor.objects.count(),
        'appointments': Appointment.objects.count(),
        'revenue': revenue,
        'pending': Appointment.objects.filter(status='Pending').count(),
        'confirmed': Appointment.objects.filter(status='Confirmed').count(),
        'cancelled': Appointment.objects.filter(status='Cancelled').count(),
        'pending_doctors': User.objects.filter(role='doctor', is_approved=False),
        'top_doctors': Doctor.objects.annotate(n=Count('appointments')).order_by('-n')[:5],
        'recent': Appointment.objects.select_related('patient', 'doctor')[:8],
    })


@staff_member_required
@require_POST
def approve_doctor(request, pk):
    User = get_user_model()
    user = get_object_or_404(User, pk=pk, role='doctor')
    user.is_approved = True
    user.save(update_fields=['is_approved'])
    messages.success(request, f'{user.first_name} ko approve kar diya. Ab Doctors me unka profile link karein.')
    return redirect('core:admin_dashboard')