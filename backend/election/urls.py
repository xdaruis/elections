from django.urls import path, include
from rest_framework.routers import DefaultRouter

from election import views

router = DefaultRouter()
router.register('', views.ElectionViewSet)

app_name = 'election'

urlpatterns = [
  path('', include(router.urls)),
]
