from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404

from apps.core.decorators import doctor_required
from .forms import DoctorProfileForm
from .models import Doctor


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
    return render(request, 'doctors/detail.html', {'doctor': doctor})


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