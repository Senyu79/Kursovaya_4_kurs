from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    PositionViewSet, TrainerViewSet, ClientViewSet,
    MembershipViewSet, WorkoutViewSet,
)

router = DefaultRouter()
router.register(r'positions', PositionViewSet)
router.register(r'trainers', TrainerViewSet)
router.register(r'clients', ClientViewSet)
router.register(r'memberships', MembershipViewSet)
router.register(r'workouts', WorkoutViewSet)

urlpatterns = [
    path('', include(router.urls)),
]