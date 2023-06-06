"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.song import Song
from tunaapi.models.artist import Artist

class SongView(ViewSet):
    """Tuna API Songs"""
    def retrieve(self, request, pk):
        """GET request for a single song"""
        try:
            song = Song.objects.get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for a list of songs"""
        songs = Song.objects.all()
        serializer = SongSerializer(songs, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """POST request to create a song"""
        artist_id = Artist.objects.get(pk=request.data['artist_id'])
        song = Song.objects.create(
            title = request.data['title'],
            artist_id = artist_id,
            album = request.data['album'],
            length = request.data['length']
        )
        serializer = SongSerializer(song)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT request to update a song"""
        artist_id = Artist.objects.get(pk=request.data['artist_id'])
        song = Song.objects.get(pk=pk)
        song.title = request.data['title']
        song.artist_id = artist_id
        song.album = request.data['album']
        song.length = request.data['length']
        song.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE request to destroy a song"""
        song = Song.objects.get(pk=pk)
        song.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')
        depth = 1

