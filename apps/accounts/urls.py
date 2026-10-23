from django.urls import path
from . import views

app_name = 'accounts'

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('patient/', views.patient_home, name='patient_home'),
    path('doctor/', views.doctor_home, name='doctor_home'),
    path('profile/', views.profile, name='profile'),
]