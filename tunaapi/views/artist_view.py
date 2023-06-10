"""View module for handling requests about artists"""
from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.artist import Artist

class ArtistView(ViewSet):
    """Tuna API artists"""
    def retrieve(self, request, pk):
        """GET request for a single artist object"""
        try:
            artists = Artist.objects.annotate(
                song_count = Count('artist_songs')
                ).get(pk=pk)
            serializer = ArtistSerializer(artists)
            return Response(serializer.data)
        except Artist.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for a list of artist objects"""
        artists = Artist.objects.all()
        serializer = AllArtistSerializer(artists, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """POST request to create an artist object"""
        artist = Artist.objects.create(
            name = request.data['name'],
            age = request.data['age'],
            bio = request.data['bio']
        )
        serializer = ArtistSerializer(artist)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT request to update an artist object"""
        artist = Artist.objects.get(pk=pk)
        artist.name = request.data['name']
        artist.age = request.data['age']
        artist.bio = request.data['bio']
        artist.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE request to destroy an artist object"""
        artist = Artist.objects.get(pk=pk)
        artist.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""
    song_count = serializers.IntegerField(default=None)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 2

class AllArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists with no song info"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')