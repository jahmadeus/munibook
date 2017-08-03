from django.contrib import admin
from .models import RouteComment, VehicleComment, Vehicle, Stop, Route

admin.site.register(RouteComment)
admin.site.register(VehicleComment)
admin.site.register(Vehicle)
admin.site.register(Stop)
admin.site.register(Route)
