from rest_framework import serializers
from .models import Location, DisabledPerson

class LocationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Location
        fields = '__all__'

class DisabledPersonSerializer(serializers.ModelSerializer):
    class Meta:
        model = DisabledPerson
        fields = '__all__'
