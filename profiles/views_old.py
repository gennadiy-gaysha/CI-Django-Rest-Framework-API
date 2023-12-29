from rest_framework.views import APIView
from django.http import Http404
from rest_framework import status
# Response class is specifically built for the  rest framework, and provides a
# nicer interface for returning content-negotiated Web API responses that can be
# rendered to multiple formats.
from rest_framework.response import Response
from .models import Profile
from .serializers import ProfileSerializer
from drf_api.permissions import IsOwnerOrReadOnly


# APIView provides such functionality as
# - making sure you  receive Request instances in your view,
# - handling parsing errors
# - adding  context to Response objects.

class ProfileList(APIView):
    '''Django REST Framework (DRF) API view class handles HTTP GET requests'''

    def get(self, request):
        # profiles = Profile.objects.all().values()
        # return Response({'profiles': list(profiles)})
        # retrieves all instances of the Profile model from the database using
        # the objects.all() method
        profiles = Profile.objects.all()
        serializer = ProfileSerializer(profiles, many=True, context={
            'request': request})
        return Response(serializer.data)


class ProfileDetail(APIView):
    serializer_class = ProfileSerializer
    # Set the permission_classes  attribute on the ProfileDetail view
    # to an array containing our permission.
    permission_classes = [IsOwnerOrReadOnly]

    def get_object(self, pk):
        try:
            profile = Profile.objects.get(pk=pk)
            # Update the  get_object method by explicitly checking object
            # permissions before we return a profile  instance. If the user
            # does not own the profile, it will throw the 403 Forbidden  error
            # and not return the instance.
            self.check_object_permissions(self.request, profile)
            return profile
        except Profile.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        # 1) Retrieves a Profile instance based on the provided primary key (pk)
        # The ProfileSerializer is then instantiated with the retrieved profile
        # and the request object included in the context.
        profile = self.get_object(pk)
        # Creates a ProfileSerializer instance, passing the retrieved Profile
        # instance as an argument.
        # 2) Including Context:
        # context={'request': request} is used to include the request object in
        # the context when creating the serializer instance.
        # This context is then accessible within the serializer, allowing the
        # get_is_owner method to access the request object.
        # Serializing Data:
        # serializer.data returns the serialized data, including the computed
        # is_owner field, which is determined by the get_is_owner method.
        serializer = ProfileSerializer(profile, context={
            'request': request})
        # return a Response containing the serialized data of the profile
        return Response(serializer.data)

    # In the put method of the ProfileDetail class, the merging of data from the
    # database (profile) and the data from the user (the edited profile in the
    # request.data) is handled by the ProfileSerializer instance
    def put(self, request, pk):
        # Step 1: Call get_object to retrieve the Profile instance
        profile = self.get_object(pk)
        # Step 2: create a new ProfileSerializer instance, passing both the
        # retrieved Profile instance and the data from the PUT request (
        # request.data)
        # - profile: This is the Profile instance retrieved from the database
        # using the get_object method. It represents the current state of the
        # profile in the database.
        # - data=request.data: This is the data received in the PUT request
        # from the user. It typically contains the edited or updated values for
        # the profile.

        # request.data typically contains JSON data, while profile is a Python
        # object representing data retrieved from the database. The ProfileSerializer
        # facilitates the merging and processing of these two sets of data.
        serializer = ProfileSerializer(profile, data=request.data, context={
            'request': request})

        # In summary, the ProfileSerializer takes care of merging the data from the database (profile) and the user input (request.data) by updating the relevant fields in the profile instance based on the provided data.
        if serializer.is_valid():
            # Inside the ProfileSerializer class, the merging of data is handled by
            # the save method. When you call serializer.save(), the serializer checks
            # which fields have been provided in the data argument and updates the
            # corresponding fields in the profile instance with the new values. This
            # is done while respecting the validation rules defined in the serializer.
            serializer.save()
            # The Meta class inside ProfileSerializer specifies which fields should
            # be included in the serialization process. In the example, it includes
            # fields like 'name', 'email', 'content', and 'image'. These are the
            # fields that will be considered when merging data during the save operation.
            return Response(serializer.data)
        # If the serializer is not valid, return a Response containing the
        # serializer errors and a status code indicating a bad request
        # (HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
