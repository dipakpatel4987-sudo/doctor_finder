from django.contrib import admin
from .models import Doctor, Availability


class AvailabilityInline(admin.TabularInline):
    model = Availability
    extra = 1


@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'specialty', 'city', 'fee', 'experience', 'rating', 'is_available')
    list_filter = ('specialty', 'city', 'is_available')
    list_editable = ('fee', 'is_available')
    search_fields = ('name', 'city', 'phone')
    ordering = ('name',)
    inlines = [AvailabilityInline]
    fieldsets = (
        ('Login Account Link', {'fields': ('user',)}),
        ('Basic', {'fields': ('name', 'specialty', 'photo', 'is_available')}),
        ('Details', {'fields': ('experience', 'education', 'about', 'fee', 'rating')}),
        ('Contact and Location', {'fields': ('phone', 'city', 'latitude', 'longitude')}),
    )