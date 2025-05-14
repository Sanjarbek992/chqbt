# users/utils.py
from oauth2_provider.models import get_application_model
from oauthlib.common import generate_token
from oauth2_provider.models import AccessToken, RefreshToken
from django.utils import timezone
from datetime import timedelta
from django.conf import settings

Application = get_application_model()

def create_oauth2_tokens(user):
    app = Application.objects.get(client_id=settings.OAUTH2_CLIENT_ID)

    expires = timezone.now() + timedelta(hours=1)
    access_token = AccessToken.objects.create(
        user=user,
        scope='read write',
        expires=expires,
        token=generate_token(),
        application=app,
    )
    refresh_token = RefreshToken.objects.create(
        user=user,
        token=generate_token(),
        access_token=access_token,
        application=app,
    )

    return {
        'access_token': access_token.token,
        'refresh_token': refresh_token.token,
        'token_type': 'Bearer',
        'expires_in': 3600
    }
