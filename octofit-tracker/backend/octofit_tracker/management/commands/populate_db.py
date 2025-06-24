from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Leaderboard, Workout
from django.conf import settings
from pymongo import MongoClient
from datetime import timedelta
from bson import ObjectId

class Command(BaseCommand):
    help = 'Populate the database with test data for users, teams, activity, leaderboard, and workouts'

    def handle(self, *args, **kwargs):
        # Connect to MongoDB
        client = MongoClient(settings.DATABASES['default']['HOST'], settings.DATABASES['default']['PORT'])
        db = client[settings.DATABASES['default']['NAME']]

        # Drop existing collections
        db.users.drop()
        db.teams.drop()
        db.activity.drop()
        db.leaderboard.drop()
        db.workouts.drop()

        # Create users
        users = []
        for user_data in [
            {'username': 'thundergod', 'email': 'thundergod@mhigh.edu', 'password': 'thundergodpassword'},
            {'username': 'metalgeek', 'email': 'metalgeek@mhigh.edu', 'password': 'metalgeekpassword'},
            {'username': 'zerocool', 'email': 'zerocool@mhigh.edu', 'password': 'zerocoolpassword'},
            {'username': 'crashoverride', 'email': 'crashoverride@hmhigh.edu', 'password': 'crashoverridepassword'},
            {'username': 'sleeptoken', 'email': 'sleeptoken@mhigh.edu', 'password': 'sleeptokenpassword'},
        ]:
            user = User(**user_data)
            user.save()
            users.append(user)
            self.stdout.write(f"Created user: {user.username}")

        # Create teams
        team = Team(name='Blue Team')
        team.save()
        team.members.add(users[0], users[1])
        self.stdout.write("Created team: Blue Team")

        team = Team(name='Gold Team')
        team.save()
        team.members.add(users[2], users[3], users[4])
        self.stdout.write("Created team: Gold Team")

        # Create activities
        for activity_data in [
            {'user': users[0], 'activity_type': 'Cycling', 'duration': timedelta(hours=1)},
            {'user': users[1], 'activity_type': 'Crossfit', 'duration': timedelta(hours=2)},
            {'user': users[2], 'activity_type': 'Running', 'duration': timedelta(hours=1, minutes=30)},
            {'user': users[3], 'activity_type': 'Strength', 'duration': timedelta(minutes=30)},
            {'user': users[4], 'activity_type': 'Swimming', 'duration': timedelta(hours=1, minutes=15)},
        ]:
            activity = Activity(**activity_data)
            activity.save()
            self.stdout.write(f"Created activity: {activity.activity_type} for user {activity.user.username}")

        # Create leaderboard entries
        for leaderboard_data in [
            {'user': users[0], 'score': 100},
            {'user': users[1], 'score': 90},
            {'user': users[2], 'score': 95},
            {'user': users[3], 'score': 85},
            {'user': users[4], 'score': 80},
        ]:
            leaderboard_entry = Leaderboard(**leaderboard_data)
            leaderboard_entry.save()
            self.stdout.write(f"Created leaderboard entry for user {leaderboard_entry.user.username} with score {leaderboard_entry.score}")

        # Create workouts
        for workout_data in [
            {'name': 'Cycling Training', 'description': 'Training for a road cycling event'},
            {'name': 'Crossfit', 'description': 'Training for a crossfit competition'},
            {'name': 'Running Training', 'description': 'Training for a marathon'},
            {'name': 'Strength Training', 'description': 'Training for strength'},
            {'name': 'Swimming Training', 'description': 'Training for a swimming competition'},
        ]:
            workout = Workout(**workout_data)
            workout.save()
            self.stdout.write(f"Created workout: {workout.name}")

        self.stdout.write(self.style.SUCCESS('Successfully populated the database with test data.'))
