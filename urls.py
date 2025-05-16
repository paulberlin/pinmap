from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
  # index
  path('', views.index, name='index'),
  path('about', views.about, name='about'),
  # map
  path('map/<int:id>', views.pinmap, name='map'),
  # configure
  path('manage', views.manage_maps, name='manage_maps'), # list of maps and new map
  path('manage/map/<int:id>', views.manage_maps_details, name='manage_maps_details'), # list of layers and new layer
  path('manage/map/<int:id>/edit', views.manage_maps_edit, name='manage_maps_edit'), # edit map
  path('manage/layer/<int:id>/edit', views.manage_maps_layer, name='manage_maps_layer'), # edit layer
  #path('manage/map/<int:id>/layer/<int:lid>', views.manage_maps_layers, name='manage_maps_layers'),
  # admin
  path('admin/', admin.site.urls),
  path("accounts/", include("django.contrib.auth.urls")),
  path("accounts/signup", views.signup, name='signup'),
]
