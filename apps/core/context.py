def layout(request):
    """Login user ke role se sahi layout template chunta hai."""
    user = request.user
    if not user.is_authenticated:
        return {'layout': 'layouts/base.html'}
    if user.role == 'doctor':
        return {'layout': 'layouts/doctor.html'}
    if user.role == 'patient':
        return {'layout': 'layouts/patient.html'}
    return {'layout': 'layouts/base.html'}