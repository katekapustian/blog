from django.core.management.base import BaseCommand
from django.conf import settings


class Command(BaseCommand):
    help = 'Clear the cart session data'

    def handle(self, *args, **kwargs):
        from django.contrib.sessions.models import Session

        sessions = Session.objects.all()
        for session in sessions:
            data = session.get_decoded()
            if settings.CART_SESSION_ID in data:
                del data[settings.CART_SESSION_ID]
                session.session_data = Session.objects.encode(data)
                session.save()

        self.stdout.write(self.style.SUCCESS('Successfully cleared cart session data'))
