from django.contrib import admin
from .models import Appointment, Review


@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    list_display = ('patient', 'doctor', 'date', 'time', 'status', 'created_at')
    list_filter = ('status', 'date', 'doctor')
    search_fields = ('patient__email', 'patient__first_name', 'doctor__name')
    list_editable = ('status',)


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('doctor', 'patient', 'rating', 'created_at')
    list_filter = ('rating', 'doctor')
    search_fields = ('doctor__name', 'patient__email', 'comment')