from rest_framework import serializers

from core.models import Election, Candidate


class ElectionListSerializer(serializers.ModelSerializer):
  class Meta:
    model = Election
    fields = ['slug', 'title']


class ElectionDetailSerializer(serializers.ModelSerializer):
  class Meta:
    model = Election
    fields = '__all__'


class CandidateSerializer(serializers.ModelSerializer):
  username = serializers.SerializerMethodField()
  votes = serializers.SerializerMethodField()

  class Meta:
    model = Candidate
    fields = ['username', 'description', 'votes']
    read_only_fields = ['username', 'votes']

  def get_username(self, obj):
    return obj.user.username

  def get_votes(self, obj):
    return getattr(obj, 'vote_count', 0)
