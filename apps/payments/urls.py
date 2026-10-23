from django.urls import path
from . import views

app_name = 'payments'

urlpatterns = [
    path('summary/<int:appt_id>/', views.summary, name='summary'),
    path('pay/<int:appt_id>/', views.pay, name='pay'),
    path('complete/<int:appt_id>/', views.complete, name='complete'),
    path('success/<int:appt_id>/', views.success, name='success'),
    path('failed/<int:appt_id>/', views.failed, name='failed'),
    path('history/', views.history, name='history'),
]