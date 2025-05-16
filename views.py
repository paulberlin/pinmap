import os
from django.shortcuts import render
from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import get_list_or_404
from django.conf import settings
from django.contrib import messages
from django.contrib.auth import login

from .models import Map
from .models import Layer
from .models import Rectangle
from .models import User

from .forms import NewMap
from .forms import ModifyMap
from .forms import ModifyLayer
from .forms import NewLayer
from .forms import SignupForm

def about(request):
  map_count = Map.objects.all().count()
  layer_count = Layer.objects.all().count()
  rect_count = Rectangle.objects.all().count()
  context = { "map_count": map_count, "layer_count": layer_count, "rect_count": rect_count }
  return render(request, 'about.html', context)

def signup(request):
  if request.user.is_authenticated:
    return redirect('index')
  form = SignupForm()
  if request.method == 'POST':
     user = User.objects.filter(email__exact=request.POST.get('email')).first()
     if user:
       messages.warning(request, 'Email address already in use.')
       return redirect('login')
     else:
       form = SignupForm(request.POST)
       if form.is_valid():
         user = form.save()
         if user:
           login(request, user)
           return redirect('index')
  context = { "form": form }
  return render(request, 'registration/signup.html', context)

def index(request):
  if request.user.is_authenticated:
    layer_count = Layer.objects.filter(owner=request.user).count()
    rect_count = Rectangle.objects.filter(owner=request.user).count()
    map_count = Map.objects.filter(owner=request.user).count()
    if map_count == 0:
      new_map = Map(owner=request.user, name='Default')
      new_map.save()
    maps = Map.objects.filter(owner__exact=request.user)
    rect_percent = rect_count / 18856 * 100;
    context = { "layer_count": layer_count, "rect_count": rect_count, "rect_percent": rect_percent, "maps": maps,  }
    return render(request, 'index.html', context)
  else:
    return redirect('login')

def manage_maps_layer(request, id):
  if request.user.is_authenticated:
    layer = get_object_or_404(Layer, pk=id, owner=request.user)
    if request.method == 'POST':
      if request.POST.get('delete') == "on":
        layer.delete()
        messages.success(request, 'Layer <em>' + layer.name + '</em> deleted.')
      else:
        # ensure we're getting a correct pinmap within the form:
        pinmap = get_object_or_404(Map, pk=request.POST.get('pinmap'), owner=request.user)
        layer_form = ModifyLayer(request.POST, instance=layer)
        if layer_form.is_valid():
          # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
          if layer_form.cleaned_data['owner'] != request.user:
            return redirect('index')
          print ("vor layer save\n")
          layer_form.save()
          messages.success(request, 'Layer <em>' + layer.name + '</em> updated.')
        else:
          # fetch again to have the old name
          layer = get_object_or_404(Layer, pk=id, owner=request.user)
          error = 'Layer <em>' + layer.name + '</em> was not updated: '
          if '__all__' in layer_form.errors:
            error += layer_form.errors['__all__'][0]
          messages.warning(request, error)
    return redirect('manage_maps_details', layer.pinmap.id)
  else:
    return redirect('login')



def manage_maps_edit(request, id):
  if request.user.is_authenticated:
    if request.method == 'POST':
      pinmap = get_object_or_404(Map, pk=id, owner=request.user)
      if request.POST.get('delete') == "on":
        pinmap.delete()
        messages.success(request, 'Map <em>' + pinmap.name + '</em> deleted.')
      else:
        edit_form = ModifyMap(request.POST, instance=pinmap)
        if edit_form.is_valid():
          # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
          if edit_form.cleaned_data['owner'] != request.user:
            return redirect('index')
          edit_form.save()
          messages.success(request, 'Map <em>' + pinmap.name + '</em> updated.')
        else:
          # fetch again to have the old name
          pinmap = get_object_or_404(Map, pk=id, owner=request.user)
          messages.warning(request, 'Map <em>' + pinmap.name + '</em> was not updated: ' + edit_form.errors['__all__'][0])
      return redirect("manage_maps")
  else:
    return redirect('login')



def manage_maps_details(request, id):
  if request.user.is_authenticated:
    pinmap = get_object_or_404(Map, pk=id, owner=request.user)
    new_layer = Layer(pinmap=pinmap, owner=request.user)
    layer_form = ""
    openform = ""
    if request.method == 'POST':
      layer_form = NewLayer(request.POST, prefix="new")
      if layer_form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if layer_form.cleaned_data['owner'] != request.user:
          return redirect('index')
        layer_form.save()
        # we re-instantiate the layer so that it's empty for the next one
        layer_form = NewLayer(instance=new_layer, prefix="new")
      else:
        openform = "open"
    else:
      layer_form = NewLayer(instance=new_layer, prefix="new")
    edit_form = ModifyLayer(instance=new_layer)
    layers = Layer.objects.filter(owner__exact=request.user).filter(pinmap=pinmap)
    context = { "highlight": "manage_maps", "map": pinmap, "layers": layers, 
      "new_layer_form": layer_form, "openform": openform, "edit_layer_form": edit_form  }
    return render(request, 'manage_maps_details.html', context)
  else:
    return redirect('login')


def manage_maps(request):
  if request.user.is_authenticated:
    openform = ""
    new_map = Map(owner=request.user)
    new_form = NewMap(instance=new_map, prefix="new")
    if request.method == 'POST':
      new_form = NewMap(request.POST, prefix="new")
      if new_form.is_valid():
        # when we're trying to get hacked by someone putting a different owner id field in the form we avoid that
        if new_form.cleaned_data['owner'] != request.user:
          return redirect('index')
        new_form.save()
      else:
        openform = "open"
    edit_form = ModifyMap(instance=new_map)
    maps = Map.objects.filter(owner__exact=request.user)
    context = { "highlight": "manage_maps", "maps": maps, "edit_form": edit_form, "new_form": new_form, "openform": openform }
    return render(request, 'manage_maps.html', context)
  else:
    return redirect('login')

def pinmap(request, id):
  if request.user.is_authenticated:
    pinmap = get_object_or_404(Map, pk=id, owner=request.user)
    layer_count = Layer.objects.filter(owner__exact=request.user).filter(pinmap=pinmap).count()
    if layer_count == 0:
      new_layer = Layer(owner=request.user, pinmap=pinmap, name='Default')
      new_layer.save()
    if request.method == 'POST':
      # save map defaults
      pinmap.zoom = request.POST.get('zoom')
      pinmap.lat = request.POST.get('lat')
      pinmap.lng = request.POST.get('lng')
      pinmap.save()

      # remove old rects
      Rectangle.objects.filter(owner__exact=request.user).filter(pinmap__exact=pinmap).delete()
      for r in request.POST.get('rects').split(";"):
        layer_id,lat1,lng1,lat2,lng2 = r.split(",")
        layer = Layer.objects.filter(owner__exact=request.user).filter(pinmap=pinmap).filter(pk=layer_id).first()
        if layer:
          rect = Rectangle(owner=request.user, pinmap=pinmap, layer=layer, lat1=lat1, lng1=lng1, lat2=lat2, lng2=lng2)
          rect.save()
    layers = Layer.objects.filter(owner__exact=request.user).filter(pinmap=pinmap)
    rects = Rectangle.objects.filter(owner__exact=request.user).filter(pinmap__exact=pinmap)
    context = { "layers": layers, "rects": rects, "map": pinmap, "highlight": "pin_maps" }
    return render(request, 'map.html', context)
  else:
    return redirect('login')
