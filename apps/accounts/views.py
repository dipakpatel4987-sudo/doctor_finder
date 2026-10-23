from django.shortcuts import render
from apps.appointments.models import Appointment
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST

from apps.core.decorators import patient_required, doctor_required
from .forms import SignupForm, LoginForm


def signup_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    form = SignupForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        user = form.save()
        if user.role == 'doctor':
            messages.success(request, 'Account ban gaya. Admin approval ke baad aapka Doctor Panel khulega.')
        else:
            messages.success(request, 'Account ban gaya. Ab login karein.')
        return redirect('accounts:login')
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('accounts:dashboard')
    form = LoginForm(request, data=request.POST or None)
    if request.method == 'POST' and form.is_valid():
        login(request, form.get_user())
        return redirect('accounts:dashboard')
    return render(request, 'accounts/login.html', {'form': form})


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, 'Logout ho gaya.')
    return redirect('accounts:login')


@login_required
def dashboard(request):
    """Role dekh kar sahi panel par bhejta hai."""
    user = request.user
    if user.is_superuser or user.role == 'admin':
        return redirect('/admin/')
    if user.role == 'doctor':
        if user.is_approved:
            return redirect('accounts:doctor_home')
        return render(request, 'accounts/doctor_pending.html')
    return redirect('accounts:patient_home')

@patient_required
def patient_home(request):
    appts = Appointment.objects.filter(patient=request.user)
    return render(request, 'accounts/patient_home.html', {
        'total': appts.count(),
        'pending': appts.filter(status='Pending').count(),
        'confirmed': appts.filter(status='Confirmed').count(),
        'cancelled': appts.filter(status='Cancelled').count(),
    })


@doctor_required
def doctor_home(request):
    profile = getattr(request.user, 'doctor_profile', None)
    appts = Appointment.objects.filter(doctor=profile) if profile else Appointment.objects.none()
    return render(request, 'accounts/doctor_home.html', {
        'profile': profile,
        'total': appts.count(),
        'pending': appts.filter(status='Pending').count(),
        'confirmed': appts.filter(status='Confirmed').count(),
        'cancelled': appts.filter(status='Cancelled').count(),
    })