"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.artist import Artist

class ArtistView(ViewSet):
    """Tuna API artists"""
    def retrieve(self, request, pk):
        """GET request for a single artist object"""
        try:
            artist = Artist.objects.get(pk=pk)
            serializer = ArtistSerializer(artist)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""
    class Meta:
        model = Artist
        fields = ('name', 'age', 'bio')
