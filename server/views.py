from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from django.contrib.auth import login, authenticate
from rest_framework import viewsets
from .models import UserProfile,TrainerProfile,Exercise,FitnessPlan,WorkoutPlan
from .serializers import UserProfileSerializer,TrainerProfileSerializer,ExerciseSerializer,FitnessPlanSerializer,WorkoutPlanSerializer
from .permissions import IsOwnerOrReadOnly,IsOwnerOrReadOnlyPlan  # Import the custom permission
from .permissions import IsOwnerOrReadOnlyTrainer  # Import trainer permissions
#from .filters import RoleFilter, TrainerRoleFilter  # Import the filter classes

@api_view(['POST'])
def register_user(request):
    if request.method == 'POST':
        serializer = CustomUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)  # Log the user in after registration
            return Response({'message': 'Registration successful'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
def user_login(request):
    if request.method == 'POST':
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return Response({'message': 'Login successful'}, status=status.HTTP_200_OK)
        return Response({'message': 'Invalid login credentials'}, status=status.HTTP_401_UNAUTHORIZED)





#fgda

class UserProfileViewSet(viewsets.ModelViewSet):
    serializer_class = UserProfileSerializer
    permission_classes = [IsOwnerOrReadOnly]

    def get_queryset(self):
        queryset = UserProfile.objects.all()

        # Extract the 'is_trainer' query parameter and filter if present
        is_trainer = self.request.query_params.get('is_trainer')
        if is_trainer is not None:
            # Convert the string 'true' or 'false' to a boolean
            is_trainer = is_trainer.lower() == 'true'
            queryset = queryset.filter(user__is_trainer=is_trainer)

        return queryset

    # ... (your view methods)

class TrainerProfileViewSet(viewsets.ModelViewSet):
    serializer_class = TrainerProfileSerializer
    permission_classes = [IsOwnerOrReadOnlyTrainer]

    def get_queryset(self):
        queryset = TrainerProfile.objects.all()

        # Extract the 'is_trainer' query parameter and filter if present
        is_trainer = self.request.query_params.get('is_trainer')
        if is_trainer is not None:
            # Convert the string 'true' or 'false' to a boolean
            is_trainer = is_trainer.lower() == 'true'
            queryset = queryset.filter(user__is_trainer=is_trainer)

        return queryset
    

class ExerciseViewSet(viewsets.ModelViewSet):
    queryset = Exercise.objects.all()
    serializer_class = ExerciseSerializer

class FitnessPlanViewSet(viewsets.ModelViewSet):
    queryset = FitnessPlan.objects.all()
    serializer_class = FitnessPlanSerializer


class AddExerciseToFitnessPlan(APIView):
    def post(self, request, pk):
        try:
            fitness_plan = FitnessPlan.objects.get(pk=pk)
        except FitnessPlan.DoesNotExist:
            return Response({'detail': 'FitnessPlan not found'}, status=status.HTTP_404_NOT_FOUND)

        exercise_data = request.data
        exercise = Exercise.objects.create(**exercise_data)
        fitness_plan.exercises.add(exercise)
        serializer = FitnessPlanSerializer(fitness_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UpdateExerciseInFitnessPlan(APIView):
    def put(self, request, pk, exercise_pk):
        try:
            fitness_plan = FitnessPlan.objects.get(pk=pk)
            exercise = Exercise.objects.get(pk=exercise_pk)
        except (FitnessPlan.DoesNotExist, Exercise.DoesNotExist):
            return Response({'detail': 'FitnessPlan or Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

        exercise_data = request.data
        for attr, value in exercise_data.items():
            setattr(exercise, attr, value)
        exercise.save()
        
        serializer = FitnessPlanSerializer(fitness_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)

class DeleteExerciseFromFitnessPlan(APIView):
    def delete(self, request, pk, exercise_pk):
        try:
            fitness_plan = FitnessPlan.objects.get(pk=pk)
            exercise = Exercise.objects.get(pk=exercise_pk)
        except (FitnessPlan.DoesNotExist, Exercise.DoesNotExist):
            return Response({'detail': 'FitnessPlan or Exercise not found'}, status=status.HTTP_404_NOT_FOUND)

        fitness_plan.exercises.remove(exercise)
        exercise.delete()
        
        serializer = FitnessPlanSerializer(fitness_plan)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


 # You'll need to create this permission class

class WorkoutPlanViewSet(viewsets.ModelViewSet):
    serializer_class = WorkoutPlanSerializer
    permission_classes = [IsOwnerOrReadOnlyPlan]  # Implement this permission class to restrict access

    def get_queryset(self):
        queryset = WorkoutPlan.objects.all()
        # Modify the queryset to filter by trainer, subscribed plans, etc., as needed
        return queryset
