from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

# Define models if not already defined in Django app (for demonstration)
# In a real app, these would be in models.py and imported
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

User = get_user_model()

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Connect to MongoDB directly for index creation
        client = MongoClient('mongodb://localhost:27017/')
        db = client['octofit_db']
        db.users.drop()
        db.teams.drop()
        db.activities.drop()
        db.leaderboard.drop()
        db.workouts.drop()
        db.users.create_index([('email', 1)], unique=True)

        # Sample users (superheroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'dc'},
            {'username': 'superman', 'email': 'superman@dc.com', 'team': 'dc'},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {'name': 'marvel'},
            {'name': 'dc'},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {'user': 'ironman', 'type': 'run', 'duration': 30},
            {'user': 'batman', 'type': 'cycle', 'duration': 45},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'marvel', 'points': 100},
            {'team': 'dc', 'points': 90},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Pushups', 'difficulty': 'easy'},
            {'name': 'Deadlift', 'difficulty': 'hard'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
