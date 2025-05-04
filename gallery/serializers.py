from rest_framework import serializers
from .models import Route, Point

class PointSerializer(serializers.ModelSerializer):
    class Meta:
        model = Point
        fields = ['id', 'x', 'y']
    
    def validate_x(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("X coordinate must be between 0 and 100.")
        return value

    def validate_y(self, value):
        if value < 0 or value > 100:
            raise serializers.ValidationError("Y coordinate must be between 0 and 100.")
        return value

class RouteSerializer(serializers.ModelSerializer):
    points = PointSerializer(many=True, read_only=True)

    class Meta:
        model = Route
        fields = ['id', 'name', 'background', 'points']
