from rest_framework import serializers
from .models import Position, Trainer, Client, Membership, Workout


class PositionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Position
        fields = '__all__'

    def validate_salary(self, value):
        if value < 0:
            raise serializers.ValidationError("Оклад не может быть отрицательным.")
        return value


class TrainerSerializer(serializers.ModelSerializer):
    position_name = serializers.CharField(source='position.name', read_only=True)

    class Meta:
        model = Trainer
        fields = ['id', 'first_name', 'last_name', 'middle_name',
                  'phone', 'email', 'position', 'position_name']


class ClientSerializer(serializers.ModelSerializer):
    full_name = serializers.CharField(source='__str__', read_only=True)

    class Meta:
        model = Client
        fields = ['id', 'first_name', 'last_name', 'middle_name', 
                  'phone', 'email', 'full_name']


class MembershipSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.__str__', read_only=True)

    class Meta:
        model = Membership
        fields = ['id', 'client', 'client_name', 'type',
                  'start_date', 'end_date', 'price']

    def validate_price(self, value):
        if value < 0:
            raise serializers.ValidationError("Цена не может быть отрицательной.")
        return value

    def validate(self, data):
        start = data.get('start_date')
        end = data.get('end_date')
        if start and end and end <= start:
            raise serializers.ValidationError(
                {"end_date": "Дата окончания должна быть позже даты начала."}
            )
        return data


class WorkoutSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.__str__', read_only=True)
    trainer_name = serializers.CharField(source='trainer.__str__', read_only=True)

    class Meta:
        model = Workout
        fields = ['id', 'client', 'client_name', 'trainer', 'trainer_name',
                  'workout_date', 'status']