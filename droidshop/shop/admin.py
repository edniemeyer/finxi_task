from django.contrib import admin
from .models import Demand

class DemandAdmin(admin.ModelAdmin):
    list_display = ['description', 'address', 'info', 'advertiser', 'status', 'image_tag']
    readonly_fields = ['image_tag']

admin.site.register(Demand, DemandAdmin)
