from rest_framework import viewsets
from rest_framework.filters import SearchFilter
from django_filters.rest_framework import DjangoFilterBackend

from .models import Position, Trainer, Client, Membership, Workout
from .serializers import (
    PositionSerializer, TrainerSerializer, ClientSerializer,
    MembershipSerializer, WorkoutSerializer,
)


class PositionViewSet(viewsets.ModelViewSet):
    queryset = Position.objects.all()
    serializer_class = PositionSerializer


class TrainerViewSet(viewsets.ModelViewSet):
    queryset = Trainer.objects.all()
    serializer_class = TrainerSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_fields = ['position']
    search_fields = ['first_name', 'last_name']


class ClientViewSet(viewsets.ModelViewSet):
    queryset = Client.objects.all()
    serializer_class = ClientSerializer
    filter_backends = [SearchFilter]
    search_fields = ['first_name', 'last_name', 'phone']


class MembershipViewSet(viewsets.ModelViewSet):
    queryset = Membership.objects.all()
    serializer_class = MembershipSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'type']


class WorkoutViewSet(viewsets.ModelViewSet):
    queryset = Workout.objects.all()
    serializer_class = WorkoutSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['status', 'trainer', 'client']