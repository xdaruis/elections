from django.contrib.auth import get_user_model, authenticate
from django.utils.translation import gettext as t
from rest_framework import serializers


class UserSerializer(serializers.ModelSerializer):
  class Meta:
    model = get_user_model()
    fields = ['username', 'name', 'email', 'password']
    extra_kwargs = {'password': {'write_only': True, 'min_length': 8}}

  def create(self, validated_data):
    return get_user_model().objects.create_user(**validated_data)

  def update(self, instance, validated_data):
    password = validated_data.pop('password', None)
    user = super().update(instance, validated_data)

    if password:
      user.set_password(password)
      user.save()

    return user


class AuthTokenSerializer(serializers.Serializer):
  username = serializers.CharField()
  password = serializers.CharField(
    style={'input_type': 'password'},
    trim_whitespace=False
  )

  def validate(self, user_data):
    username = user_data.get('username')
    password = user_data.get('password')

    user = authenticate(
      request=self.context.get('request'),
      username=username,
      password=password,
    )

    if not user:
      message = t('Wrong username or password')
      raise serializers.ValidationError(message, code='authorization')

    user_data['user'] = user
    return user_data
