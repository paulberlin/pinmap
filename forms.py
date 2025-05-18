from django import forms
from django.contrib.auth.forms import UserCreationForm
from simplemathcaptcha.fields import MathCaptchaField
import re

from .models import Map
from .models import Layer
from .models import Rectangle
from .models import User


class SignupForm(UserCreationForm):
  email = forms.EmailField(max_length=200, help_text='Required')
  captcha = MathCaptchaField()

  class Meta:
    model = User
    fields = ('username', 'email', 'password1', 'password2')



class ModifyMap(forms.ModelForm):
  delete = forms.BooleanField(label='Delete', help_text="When you delete a Map, all its Layers and Rectangles are deleted as well.", required=False)

  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

  #def clean_public_name(self):
  #  data = self.cleaned_data['public_name']
  #  return cleanup2(data)

  class Meta:
    model = Map
    fields = ('__all__')
    labels = {
      "name": "The name of the map",
    }
    widgets = {
      "owner": forms.HiddenInput(),
    }
    exclude = ['zoom', 'lat', 'lng', 'public_name']


class NewMap(forms.ModelForm):
  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

  class Meta:
    model = Map
    fields = ('__all__')
    labels = {
      "name": "The name of the map",
    }
    widgets = {
      "owner": forms.HiddenInput(),
    }
    exclude = ['zoom', 'lat', 'lng', 'public_name']


class NewLayer(forms.ModelForm):

  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

  def clean_color(self):
    data = self.cleaned_data['color']
    return cleanup(data)

  class Meta:
    model = Layer
    fields = ('__all__')
    labels = {
      "name": "The name of the layer",
    }
    widgets = {
      "owner": forms.HiddenInput(),
      "pinmap": forms.HiddenInput(),
      "color": forms.ColorInput(),
    }



class ModifyLayer(forms.ModelForm):
  delete = forms.BooleanField(label='Delete', help_text="When you delete a Layer, all its Rectangles are deleted as well.", required=False)

  def clean_name(self):
    data = self.cleaned_data['name']
    return cleanup(data)

  def clean_color(self):
    data = self.cleaned_data['color']
    return cleanup(data)

  class Meta:
    model = Layer
    fields = ('__all__')
    labels = {
      "name": "The name of the layer",
    }
    widgets = {
      "owner": forms.HiddenInput(),
      "pinmap": forms.HiddenInput(),
      "color": forms.ColorInput(),
    }






def cleanup(str):
  return str.replace('"', '``').replace("'", "`").replace('<', '').replace('>', '')
def cleanup2(str):
  return re.sub(r'[^\x20-\x7E]',r'_', str)
