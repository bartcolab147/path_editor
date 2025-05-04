from django import forms
from .models import Route, Point

class RouteForm(forms.ModelForm):
    class Meta:
        model = Route
        fields = ['name', 'background']

class PointForm(forms.ModelForm):
    x = forms.FloatField(min_value=0, max_value=100, label="X Coordinate (%)")
    y = forms.FloatField(min_value=0, max_value=100, label="Y Coordinate (%)")

    class Meta:
        model = Point
        fields = ['x', 'y']
