from rest_framework import serializers
from .models import CustomUser, UserProfile,TrainerProfile,Exercise,FitnessPlan,WorkoutPlan

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ('id', 'username', 'email', 'is_trainer', 'password')

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            username=validated_data['username'],
            is_trainer=validated_data['is_trainer']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user






class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = '__all__'


class TrainerProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = TrainerProfile
        fields = '__all__'


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = '__all__'

class FitnessPlanSerializer(serializers.ModelSerializer):
    exercises = ExerciseSerializer(many=True)

    class Meta:
        model = FitnessPlan
        fields = '__all__'

    def create(self, validated_data):
        exercises_data = validated_data.pop('exercises')
        fitness_plan = FitnessPlan.objects.create(**validated_data)
        for exercise_data in exercises_data:
            exercise = Exercise.objects.create(**exercise_data)
            fitness_plan.exercises.add(exercise)
        return fitness_plan
    

class WorkoutPlanSerializer(serializers.ModelSerializer):
    class Meta:
        model = WorkoutPlan
        fields = '__all__'  # Include all fields for serialization