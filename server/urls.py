from django.urls import path,include
from . import views
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet,TrainerProfileViewSet,ExerciseViewSet,FitnessPlanViewSet,AddExerciseToFitnessPlan,DeleteExerciseFromFitnessPlan,UpdateExerciseInFitnessPlan,WorkoutPlanViewSet

router = DefaultRouter()
router.register(r'user-profiles', UserProfileViewSet, basename='user-profile')
router.register(r'trainer-profiles', TrainerProfileViewSet, basename='trainer-profile')
router.register(r'exercises', ExerciseViewSet)
router.register(r'fitnessplans', FitnessPlanViewSet)
router.register(r'workout-plans', WorkoutPlanViewSet,basename='workout-plan')
urlpatterns = [
    path('api/', include(router.urls)),
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', views.user_login, name='user_login'),
    path('fitnessplans/<int:pk>/add_exercise/', AddExerciseToFitnessPlan.as_view(), name='add-exercise-to-fitnessplan'),
    path('fitnessplans/<int:pk>/update_exercise/<int:exercise_pk>/', UpdateExerciseInFitnessPlan.as_view(), name='update-exercise-in-fitnessplan'),
    path('fitnessplans/<int:pk>/delete_exercise/<int:exercise_pk>/', DeleteExerciseFromFitnessPlan.as_view(), name='delete-exercise-from-fitnessplan'),
    # Add more URL patterns for your application as needed
]
