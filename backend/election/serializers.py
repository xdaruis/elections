from rest_framework import serializers

from core.models import Election


class ElectionListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Election
    fields = ['slug', 'title']


class ElectionDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Election
    fields = '__all__'
