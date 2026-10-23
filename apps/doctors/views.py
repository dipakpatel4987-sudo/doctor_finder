from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from apps.core.decorators import doctor_required
from .forms import DoctorProfileForm
from .forms_availability import AvailabilityForm
from .models import Doctor, Availability


def doctor_list(request):
    qs = Doctor.objects.filter(is_available=True)
    q = request.GET.get('q', '').strip()
    spec = request.GET.get('specialty', '').strip()
    city = request.GET.get('city', '').strip()

    if q:
        qs = qs.filter(Q(name__icontains=q) | Q(specialty__icontains=q))
    if spec:
        qs = qs.filter(specialty=spec)
    if city:
        qs = qs.filter(city__icontains=city)

    page = Paginator(qs, 6).get_page(request.GET.get('page'))

    params = request.GET.copy()
    params.pop('page', None)

    return render(request, 'doctors/list.html', {
        'page': page,
        'specialties': [s[0] for s in Doctor.SPECIALTIES],
        'q': q, 'spec': spec, 'city': city,
        'querystring': params.urlencode(),
    })


def doctor_detail(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk, is_available=True)
    reviews = doctor.reviews.select_related('patient')[:10]
    return render(request, 'doctors/detail.html', {
        'doctor': doctor,
        'reviews': reviews,
        'review_count': doctor.reviews.count(),
    })


def doctor_map(request):
    data = [
        {
            'id': d.id, 'name': d.name, 'specialty': d.specialty, 'city': d.city,
            'phone': d.phone, 'lat': d.latitude, 'lng': d.longitude,
        }
        for d in Doctor.objects.filter(is_available=True,
                                       latitude__isnull=False, longitude__isnull=False)
    ]
    return render(request, 'doctors/map.html', {'doctors_data': data})


@doctor_required
def doctor_edit(request):
    profile = getattr(request.user, 'doctor_profile', None)
    if profile is None:
        messages.error(request, 'Aapka account abhi Doctor profile se link nahi hai. Admin se link karwayein.')
        return redirect('accounts:doctor_home')
    form = DoctorProfileForm(request.POST or None, request.FILES or None, instance=profile)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Profile update ho gayi.')
        return redirect('doctors:edit')
    return render(request, 'doctors/edit.html', {'form': form, 'profile': profile})


@doctor_required
def availability(request):
    profile = getattr(request.user, 'doctor_profile', None)
    if profile is None:
        messages.error(request, 'Aapka account abhi Doctor profile se link nahi hai. Admin se link karwayein.')
        return redirect('accounts:doctor_home')
    form = AvailabilityForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        row = form.save(commit=False)
        row.doctor = profile
        row.save()
        messages.success(request, 'Schedule me jod diya gaya.')
        return redirect('doctors:availability')
    return render(request, 'doctors/availability.html', {
        'form': form, 'rows': profile.availability.all(),
    })


@doctor_required
@require_POST
def availability_delete(request, pk):
    profile = getattr(request.user, 'doctor_profile', None)
    row = get_object_or_404(Availability, pk=pk, doctor=profile) if profile else None
    if row:
        row.delete()
        messages.success(request, 'Schedule se hata diya gaya.')
    return redirect('doctors:availability')