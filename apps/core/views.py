from django.shortcuts import render, redirect


def home(request):
    if request.user.is_authenticated and not request.user.is_superuser:
        return redirect('accounts:dashboard')
    return render(request, 'core/home.html')