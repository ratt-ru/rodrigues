from .models import KlikoImage, Job
from rest_framework import serializers


class KlikoImageSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = KlikoImage
        fields = ('url', 'repository', 'tag', 'last_updated', 'error_message', 'state', 'available')


class JobSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Job
        fields = ('url', 'name', 'started', 'finished', 'log', 'config', 'state')
