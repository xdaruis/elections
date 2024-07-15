from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.db.models import Count, Q

from core.models import Candidate, Election
from election import serializers


@extend_schema_view(
  list=extend_schema(description='List all elections'),
  retrieve=extend_schema(description='Get details of a specific election'),
)
class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Election.objects.all().order_by('-end_date')
  lookup_field = 'slug'

  def get_serializer_class(self):
    if self.action == 'list':
      return serializers.ElectionListSerializer
    return serializers.ElectionDetailSerializer

  @action(detail=True, methods=['GET'])
  def candidates(self, request, slug=None):
    """Get candidates of a specific election"""
    election = self.get_object()
    candidates = Candidate.objects.filter(election=election).annotate(
      vote_count=Count('vote', filter=Q(vote__election=election))
    ).order_by('-vote_count')
    serializer = serializers.CandidateSerializer(candidates, many=True)
    return Response(serializer.data)
