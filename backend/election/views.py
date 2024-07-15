from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import action
from django.shortcuts import get_object_or_404
from drf_spectacular.utils import extend_schema, extend_schema_view

from core.models import Candidate, Election
from election import serializers


@extend_schema_view(
  list=extend_schema(description='List all elections'),
  retrieve=extend_schema(description='Get details of a specific election'),
  candidates=extend_schema(description='Get candidates of a specific election'),
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
    election = self.get_object()
    candidates = Candidate.objects.filter(election=election)
    serializer = serializers.CandidateSerializer(candidates, many=True)
    return Response(serializer.data)

  def get_object(self):
    queryset = self.get_queryset()
    lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    obj = get_object_or_404(queryset, **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj

  def retrieve(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)
