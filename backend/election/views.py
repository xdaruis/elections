from drf_spectacular.utils import (
  extend_schema_view,
  extend_schema
)
from rest_framework import viewsets
from django.shortcuts import get_object_or_404

from election import serializers
from core.models import Election


@extend_schema_view(
  list=extend_schema(description="List all elections"),
  retrieve=extend_schema(description="Get details of a specific election")
)
class ElectionViewSet(viewsets.ReadOnlyModelViewSet):
  queryset = Election.objects.all()
  lookup_field = 'slug'

  def get_serializer_class(self):
    if self.action == 'list':
      return serializers.ElectionListSerializer
    return serializers.ElectionDetailSerializer

  def get_object(self):
    queryset = self.get_queryset()
    lookup_url_kwarg = self.lookup_url_kwarg or self.lookup_field
    filter_kwargs = {self.lookup_field: self.kwargs[lookup_url_kwarg]}
    obj = get_object_or_404(queryset, **filter_kwargs)
    self.check_object_permissions(self.request, obj)
    return obj

  def retrieve(self, request, *args, **kwargs):
    return super().retrieve(request, *args, **kwargs)
