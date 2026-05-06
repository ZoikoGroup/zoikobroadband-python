from django.contrib import admin
from .models import BundleRequest

@admin.register(BundleRequest)
class BundleRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'phone', 'bundle_name', 'bundle_price','is_sent', 'created_at')
    search_fields = ('name', 'email', 'phone', 'bundle_name')
    list_filter = ('created_at',)
    readonly_fields = ('name', 'email', 'phone', 'bundle_name', 'bundle_price', 'created_at')
    ordering = ('-created_at',)