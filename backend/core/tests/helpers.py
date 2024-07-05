from django.contrib.auth import get_user_model

_user_id = 1


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
