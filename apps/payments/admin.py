from django.contrib import admin
from .models import Payment


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('appointment', 'amount', 'gst', 'total', 'status', 'txn_id', 'paid_at')
    list_filter = ('status',)
    search_fields = ('txn_id', 'appointment__patient__email', 'appointment__doctor__name')
    readonly_fields = ('amount', 'gst', 'total', 'txn_id', 'paid_at')