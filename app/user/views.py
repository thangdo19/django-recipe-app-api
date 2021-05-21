from rest_framework import generics
# Because we are customizing 'username' field to 'email' field,
# we must inherit from ObtainAuthToken to modify setting to
# the class variables. If not, you can use ObtainAuthToken
# directly
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings

from user.serializers import UserSerializer, AuthTokenSerializer


class CreateUserView(generics.CreateAPIView):
    """ Create a new user in the system """
    serializer_class = UserSerializer


class CreateTokenView(ObtainAuthToken):
    """ Create a new auth token for user """
    serializer_class = AuthTokenSerializer
    # Renderer classes: Render to view this
    # endpoint in the browser with the browsable API
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES
