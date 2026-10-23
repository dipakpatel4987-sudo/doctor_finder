from django.shortcuts import render, redirect

from apps.doctors.models import Doctor


def home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('accounts:dashboard')
    available = Doctor.objects.filter(is_available=True)
    return render(request, 'core/home.html', {
        'top_doctors': available[:4],
        'doctor_count': available.count(),
    })