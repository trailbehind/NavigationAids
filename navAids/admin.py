from django.contrib import admin
from models import *

class NavAidAdmin(admin.ModelAdmin):
	list_display = ('name', 'scale_max', 'scale_min', 'location')

admin.site.register(Beacon, NavAidAdmin)
admin.site.register(Buoy, NavAidAdmin)
admin.site.register(DayMarker, NavAidAdmin)
admin.site.register(Light, NavAidAdmin)
admin.site.register(Mooring, NavAidAdmin)
