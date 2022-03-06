from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework import generics, status
from django.shortcuts import get_object_or_404

from ..models.folder import Folder
from ..serializers import FolderSerializer

# Create your views here.
class FoldersView(generics.ListCreateAPIView):
    permission_classes=(IsAuthenticated,)
    serializer_class = FolderSerializer
    def get(self, request):
        """Index request"""
        # Get all the folders:
        # folders = Folder.objects.all()
        # Filter the folders by owner, so you can only see your owned folders
        folders = Folder.objects.filter(owner=request.user.id)
        # Run the data through the serializer
        data = FolderSerializer(folders, many=True).data
        return Response({ 'folders': data })

    def post(self, request):
        """Create request"""
        # Add user to request data object
        request.data['folder']['owner'] = request.user.id
        # Serialize/create folder
        folder = FolderSerializer(data=request.data['folder'])
        # If the folder data is valid according to our serializer...
        if folder.is_valid():
            # Save the created folder & send a response
            folder.save()
            return Response({ 'folder': folder.data }, status=status.HTTP_201_CREATED)
        # If the data is not valid, return a response with the errors
        return Response(folder.errors, status=status.HTTP_400_BAD_REQUEST)

class FolderDetailView(generics.RetrieveUpdateDestroyAPIView):
    permission_classes=(IsAuthenticated,)
    def get(self, request, pk):
        """Show request"""
        # Locate the folder to show
        folder = get_object_or_404(Folder, pk=pk)
        # Only want to show owned folders?
        if request.user != folder.owner:
            raise PermissionDenied('Unauthorized, you do not own this folder')

        # Run the data through the serializer so it's formatted
        data = FolderSerializer(folder).data
        return Response({ 'folder': data })

    def delete(self, request, pk):
        """Delete request"""
        # Locate folder to delete
        folder = get_object_or_404(Folder, pk=pk)
        # Check the folder's owner against the user making this request
        if request.user != folder.owner:
            raise PermissionDenied('Unauthorized, you do not own this folder')
        # Only delete if the user owns the  folder
        folder.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

    def partial_update(self, request, pk):
        """Update Request"""
        # Locate Folder
        # get_object_or_404 returns a object representation of our Folder
        folder = get_object_or_404(Folder, pk=pk)
        # Check the folder's owner against the user making this request
        if request.user != folder.owner:
            raise PermissionDenied('Unauthorized, you do not own this folder')

        # Ensure the owner field is set to the current user's ID
        request.data['folder']['owner'] = request.user.id
        # Validate updates with serializer
        data = FolderSerializer(folder, data=request.data['folder'], partial=True)
        if data.is_valid():
            # Save & send a 204 no content
            data.save()
            return Response(status=status.HTTP_204_NO_CONTENT)
        # If the data is not valid, return a response with the errors
        return Response(data.errors, status=status.HTTP_400_BAD_REQUEST)
