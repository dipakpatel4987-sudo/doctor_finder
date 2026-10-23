from django.http import JsonResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_GET, require_POST

from .forms_availability import AvailabilityForm
from .models import Availability


def _profile(request):
    u = request.user
    if not u.is_authenticated or u.role != 'doctor' or not u.is_approved:
        return None
    return getattr(u, 'doctor_profile', None)


def _row(r):
    return {
        'id': r.pk,
        'weekday': r.weekday,
        'day': r.get_weekday_display(),
        'start': r.start_time.strftime('%H:%M'),
        'end': r.end_time.strftime('%H:%M'),
    }


def _forbidden():
    return JsonResponse({'ok': False, 'errors': {'__all__': ['Ye kaam sirf approved aur linked doctor kar sakta hai.']}},
                        status=403)


def _errors(form):
    return {k: [str(e) for e in v] for k, v in form.errors.items()}


@require_GET
def availability_list(request):
    profile = _profile(request)
    if profile is None:
        return _forbidden()
    return JsonResponse({'ok': True, 'rows': [_row(r) for r in profile.availability.all()]})


@require_POST
def availability_add(request):
    profile = _profile(request)
    if profile is None:
        return _forbidden()
    form = AvailabilityForm(request.POST)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': _errors(form)}, status=400)
    row = form.save(commit=False)
    row.doctor = profile
    row.save()
    return JsonResponse({'ok': True, 'row': _row(row)})


@require_POST
def availability_update(request, pk):
    profile = _profile(request)
    if profile is None:
        return _forbidden()
    row = get_object_or_404(Availability, pk=pk, doctor=profile)
    form = AvailabilityForm(request.POST, instance=row)
    if not form.is_valid():
        return JsonResponse({'ok': False, 'errors': _errors(form)}, status=400)
    row = form.save()
    return JsonResponse({'ok': True, 'row': _row(row)})


@require_POST
def availability_delete_api(request, pk):
    profile = _profile(request)
    if profile is None:
        return _forbidden()
    row = get_object_or_404(Availability, pk=pk, doctor=profile)
    row.delete()
    return JsonResponse({'ok': True})