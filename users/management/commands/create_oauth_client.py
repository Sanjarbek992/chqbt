from django.core.management.base import BaseCommand
from oauth2_provider.models import Application
from django.contrib.auth import get_user_model

User = get_user_model()

class Command(BaseCommand):
    help = "OAuth2 client yaratish"

    def handle(self, *args, **kwargs):
        username = input("Superadmin username: ").strip()
        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("Foydalanuvchi topilmadi."))
            return

        app, created = Application.objects.get_or_create(
            name="Frontend Client",
            user=user,
            client_type=Application.CLIENT_CONFIDENTIAL,
            authorization_grant_type=Application.GRANT_PASSWORD,
        )

        self.stdout.write(self.style.SUCCESS("OAuth2 client yaratildi:"))
        self.stdout.write(f"CLIENT ID: {app.client_id}")
        self.stdout.write(f"CLIENT SECRET: {app.client_secret}")
