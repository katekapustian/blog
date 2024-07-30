from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from blog.models import Profile


class Command(BaseCommand):
    help = 'Check and create missing profiles for users'

    def handle(self, *args, **kwargs):
        users_without_profiles = User.objects.filter(profile__isnull=True)
        for user in users_without_profiles:
            Profile.objects.create(user=user)
        self.stdout.write(self.style.SUCCESS('Successfully ensured all users have profiles.'))
