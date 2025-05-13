from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError

class User(AbstractUser):
  pass

class Map(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  public_name = models.CharField(max_length=50, null=True, blank=True, unique=True)
  zoom = models.IntegerField(default=7)
  lat = models.FloatField(default=52.520008)
  lng = models.FloatField(default=13.404954)

  # Metadata
  class Meta:
    unique_together = ('owner', 'name')
  

  @property
  def how_many_layers(self):
    return Layer.objects.filter(pinmap__exact=self.id).count()

  @property
  def how_many_rectangles(self):
    return Rectangle.objects.filter(pinmap__exact=self.id).count()

  def __str__(self):
    return str(self.name)

class Layer(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  name = models.CharField(max_length=50)
  color = models.CharField(max_length=7, default='#0000FF')
  pinmap = models.ForeignKey(Map, on_delete=models.CASCADE)

  # ensure owner consistency
  def save(self, *args, **kwargs):
    if self.owner != self.pinmap.owner:
      raise ValidationError("Owner mismatch!")
    super(Layer, self).save(*args, **kwargs)

  # Metadata
  class Meta:
    unique_together = ('owner', 'pinmap', 'name')
  

  @property
  def how_many_rectangles(self):
    return Rectangle.objects.filter(layer__exact=self.id).count()


  def __str__(self):
    return self.name

class Rectangle(models.Model):
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
  layer = models.ForeignKey(Layer, on_delete=models.CASCADE)
  pinmap = models.ForeignKey(Map, on_delete=models.CASCADE)
  # we use int values only, but maybe in the future also float?
  lat1 = models.FloatField()
  lng1 = models.FloatField()  
  lat2 = models.FloatField()
  lng2 = models.FloatField()  

  # ensure owner consistency
  def save(self, *args, **kwargs):
    if self.owner != self.layer.owner:
      raise ValidationError("Owner mismatch!")
    super(Rectangle, self).save(*args, **kwargs)

  def __str__(self):
    return str(self.id)
