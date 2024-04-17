from rest_framework import serializers
from .models import VideoProcess

class VideoSerializer(serializers.ModelSerializer):
    class Meta:
        model=VideoProcess
        fields='__all__'

