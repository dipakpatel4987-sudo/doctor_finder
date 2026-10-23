from django.urls import path
from . import views

app_name = 'appointments'

urlpatterns = [
    path('book/', views.book, name='book'),
    path('mine/', views.patient_list, name='patient_list'),
    path('mine/<int:pk>/cancel/', views.patient_cancel, name='patient_cancel'),
    path('doctor/', views.doctor_list, name='doctor_list'),
    path('doctor/<int:pk>/<str:action>/', views.doctor_update, name='doctor_update'),
    path('mine/<int:pk>/reschedule/', views.patient_reschedule, name='patient_reschedule'),
]