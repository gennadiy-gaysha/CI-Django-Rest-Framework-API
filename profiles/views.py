from rest_framework.views import APIView
# Response class is specifically built for the  rest framework, and provides a
# nicer interface for returning content-negotiated Web API responses  that can be
# rendered to multiple formats.
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer

# APIView provides such functionality as
# - making sure you  receive Request instances in your view,
# - handling parsing errors
# - adding  context to Response objects.

class ProfileList(APIView):
    '''Django REST Framework (DRF) API view class handles HTTP GET requests'''

    def get(self, request):
        # retrieves all instances of the Profile model from the database using
        # the objects.all() method
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True)
        return Response(serializer.data)


