from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.
class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    is_trainer = models.BooleanField(default=False)
    trainer = models.ForeignKey('self', on_delete=models.SET_NULL, null=True, blank=True)

class UserProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    age = models.PositiveIntegerField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    height = models.DecimalField(max_digits=5, decimal_places=2)
    weight = models.DecimalField(max_digits=5, decimal_places=2)
    contact_number = models.CharField(max_length=15)
    image = models.URLField(default='https://cdn-icons-png.flaticon.com/512/5087/5087579.png',blank=True,)  # Allow the field to be empty)


class TrainerProfile(models.Model):
    GENDER_CHOICES = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Other', 'Other'),
    )

    SPECIALIZATION_CHOICES = (
        ('Yoga', 'Yoga'),
        ('Strength Training', 'Strength Training'),
        ('Cardio', 'Cardio'),
        ('Pilates', 'Pilates'),
        ('CrossFit', 'CrossFit'),
        ('Dance', 'Dance'),
        ('Functional Training', 'Functional Training'),
        ('Other', 'Other'),
    )
    trainer = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    specialization = models.CharField(max_length=50,choices=SPECIALIZATION_CHOICES,default='Other')
    experience = models.PositiveIntegerField()
    contact_number = models.CharField(max_length=15)
    image = models.URLField(default='https://cdn-icons-png.flaticon.com/512/5087/5087579.png',blank=True,)  # Allow the field to be empty)


class Exercise(models.Model):
    image = models.URLField()
    name = models.CharField(max_length=100)
    sets = models.PositiveIntegerField()
    min = models.PositiveIntegerField(default=0)
    description = models.TextField(max_length=1000,default="No description available")

class FitnessPlan(models.Model):
    name = models.CharField(max_length=100)
    image = models.URLField()
    description = models.CharField(max_length=200)
    exercises = models.ManyToManyField(Exercise)

    def __str__(self):
        return self.name
    

class WorkoutPlan(models.Model):
    plan_name = models.CharField(max_length=100)
    goal = models.CharField(max_length=50)  # You can use choices for predefined goals
    duration = models.PositiveIntegerField()  # Duration in weeks
    fitness_plan = models.ForeignKey(FitnessPlan, on_delete=models.SET_NULL, null=True, blank=True)  # Store exercises as a JSON array
    price=models.PositiveIntegerField(default=0)
    trainer = models.ForeignKey(CustomUser, on_delete=models.CASCADE)  # Trainer who created the plan
    users = models.ManyToManyField(CustomUser, related_name='subscribed_plans', blank=True)  # Users subscribed to the plan

    def __str__(self):
        return self.plan_name
    

