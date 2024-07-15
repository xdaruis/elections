from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from drf_spectacular.utils import extend_schema, extend_schema_view
from django.contrib.auth import get_user_model


from django.db.models import Count, Q
from django.utils import timezone
from django.shortcuts import get_object_or_404

from core.tests.helpers import create_vote
from core.models import Candidate, Election, Vote
from election import serializers


class IsElectionActive(permissions.BasePermission):
  def has_object_permission(self, request, view, obj):
    now = timezone.now().date()
    return obj.start_date <= now <= obj.end_date


@extend_schema_view(
  list=extend_schema(description='List all elections'),
  retrieve=extend_schema(description='Get details of a specific election'),
  vote=extend_schema(
    description='Create, modify, or delete a vote for an ongoing election',
    methods=['POST', 'PATCH', 'DELETE'],
    request={
      'application/json': {
        'type': 'object',
        'properties': {
          'candidate_username': {
            'type': 'string',
            'description': 'Username of the candidate to vote for'
          }
        },
        'required': ['candidate_username']
      }
    },
  )
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

  @action(detail=True, methods=['POST', 'DELETE', 'PATCH'],
          permission_classes=[IsAuthenticated, IsElectionActive])
  def vote(self, request, slug=None):
    """Create/Modify/Delete votes for an ongoing election"""
    election = self.get_object()
    user = request.user
    vote = Vote.objects.filter(user=user, election=election).first()

    if request.method == 'DELETE':
      if not vote:
        return Response({'error': 'You have not voted in this election'},
                        status=status.HTTP_400_BAD_REQUEST)

      vote.delete()
      return Response({'message': 'Vote deleted successfully'},
                      status=status.HTTP_200_OK)

    candidate_username = request.data.get('candidate_username')
    if not candidate_username:
      return Response({'error': 'candidate_username is required'},
                      status=status.HTTP_400_BAD_REQUEST)

    candidate_user = get_object_or_404(get_user_model(),
                                       username=candidate_username)
    candidate = get_object_or_404(Candidate,
                                  user=candidate_user,
                                  election=election)

    if request.method == 'POST':
      if vote:
        return Response({'error': 'You have already voted in this election'},
                        status=status.HTTP_400_BAD_REQUEST)

      create_vote(user, election, candidate)
      return Response({'message': 'Vote recorded successfully'},
                      status=status.HTTP_201_CREATED)

    if not vote:
      return Response({'error': 'You have not voted in this election'},
                      status=status.HTTP_400_BAD_REQUEST)

    vote.voted_candidate = candidate
    vote.save()
    return Response({'message': 'Vote updated successfully'},
                    status=status.HTTP_200_OK)
