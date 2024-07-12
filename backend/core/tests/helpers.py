from django.contrib.auth import get_user_model
from core.models import Election, Candidate

_user_id = 1
_election_id = 1


def create_user(**user_data):
  global _user_id
  user = {
    'username': f'user{_user_id}',
    'name': 'User Tester',
    'email': f'user{_user_id}@example.com',
    'password': 'password'
  }
  user.update(user_data)
  _user_id += 1
  return get_user_model().objects.create_user(**user)


def create_election(**election_data):
  global _election_id
  election = {
    'title': f'Election {_election_id}',
    'slug': f'election-{_election_id}',
    'start_date': '2024-01-01',
    'end_date': '2024-01-02',
  }
  election.update(election_data)
  _election_id += 1
  return Election.objects.create(**election)


def create_candidate(user, election):
  return Candidate.objects.create(
    user=user,
    election=election,
    description=f'Vote me! Vote now for {user}!',
  )
