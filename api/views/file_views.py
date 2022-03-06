from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.file import File
from ..serializers import FileSerializer

# Create your views here.
class FilesView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = FileSerializer
    def get(self, request):
        """Index request"""
        # Get all the folders:
        # files = File.objects.all()
        # Filter the folders by owner, so you can only see your owned files
        files = File.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = FileSerializer(files, many=True).data
        return Response({ 'files': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['file']['owner'] = request.user.id
        # Serialize/create file
        file = FileSerializer(data=request.data['file'])
        # If the file data is valid according to our serializer...
        if file.is_valid():
            # Save the created file & send a response
            file.save()
            return Response({ 'file': file.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(file.errors, status=status.HTTP_400_BAD_REQUEST)

class FileDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the file to show
        file = get_object_or_404(File, pk=pk)
        # Only want to show owned folders?
        if request.user != file.owner:
            raise PermissionDenied('Unauthorized, you do not own this file')

        # Run the data through the serializer so it's formatted
        data = FileSerializer(file).data
        return Response({ 'file': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate file to delete
        file = get_object_or_404(File, pk=pk)
        # Check the file's owner against the user making this request
        if request.user != file.owner:
            raise PermissionDenied('Unauthorized, you do not own this file')
        # Only delete if the user owns the  file
        file.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate File
        # get_object_or_404 returns a object representation of our File
        file = get_object_or_404(File, pk=pk)
        # Check the file's owner against the user making this request
        if request.user != file.owner:
            raise PermissionDenied('Unauthorized, you do not own this file')

        # Ensure the owner field is set to the current user's ID
        request.data['file']['owner'] = request.user.id
        # Validate updates with serializer
        data = FileSerializer(file, data=request.data['file'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
