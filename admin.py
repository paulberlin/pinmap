from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User
from .models import Map
from .models import Layer
from .models import Rectangle


class MapAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner', 'public_name')

class LayerAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner', 'pinmap', 'color')

class RectangleAdmin(admin.ModelAdmin):
  list_display = ('__str__', 'owner', 'pinmap', 'layer', 'lat1', 'lng1', 'lat2', 'lng2')

admin.site.register(User, UserAdmin)
admin.site.register(Map, MapAdmin)
admin.site.register(Layer, LayerAdmin)
admin.site.register(Rectangle, RectangleAdmin)


