from django.contrib import admin
from django.db import models  # Import the models module

from .models import Instagram_acaunts, acaunts_for_get, Potoci
# Register your models here.
admin.site.register(Instagram_acaunts)

class Admin_Acaunts(admin.ModelAdmin):
    list_display = ('acaunts_href', 'used', 'send_massage_point')
    search_fields = ['acaunts_href', 'used', 'send_massage_point']
    list_filter = ('used', 'send_massage_point')

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.annotate(
            used_count=models.Count('used'),
            send_massage_count=models.Count('send_massage_point')
        )
        return queryset

    def used_count(self, obj):
        return obj.used_count
    used_count.short_description = 'Used Count'

    def send_massage_count(self, obj):
        return obj.send_massage_count
    send_massage_count.short_description = 'Send Massage Count'

# Register your model with the admin class
admin.site.register(acaunts_for_get, Admin_Acaunts)
admin.site.register(Potoci)
