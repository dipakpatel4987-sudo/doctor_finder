from functools import wraps
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect


def patient_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        if request.user.role != 'patient':
            return redirect('accounts:dashboard')
        return view(request, *args, **kwargs)
    return wrapper


def doctor_required(view):
    @wraps(view)
    @login_required
    def wrapper(request, *args, **kwargs):
        u = request.user
        if u.role != 'doctor' or not u.is_approved:
            return redirect('accounts:dashboard')
        return view(request, *args, **kwargs)
    return wrapper