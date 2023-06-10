"""View module for handling requests about songs"""
from django.http import HttpResponseServerError
from django.db.models import Count
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from rest_framework.decorators import action
from tunaapi.models.song import Song
from tunaapi.models.artist import Artist
from tunaapi.models.genre import Genre
from tunaapi.models.songgenre import SongGenre

class SongView(ViewSet):
    """Tuna API Songs"""
    def retrieve(self, request, pk):
        """GET request for a single song"""
        try:
            song = Song.objects.annotate(
                genre_count=Count('genres')
                ).get(pk=pk)
            serializer = SongSerializer(song)
            return Response(serializer.data)
        except Song.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for a list of songs"""
        songs = Song.objects.all()
        serializer = AllSongSerializer(songs, many=True, context={'request': request})
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

    @action(methods=['post'], detail=True)
    def add_genre(self, request, pk):
        """POST request to add genres to a song"""
        song = Song.objects.get(pk=pk)
        genre = Genre.objects.get(id=request.data['genre'])
        SongGenre.objects.create(song_id=song, genre_id=genre)
        return Response({'message': 'New genre added'}, status=status.HTTP_201_CREATED)

    @action(methods=['delete'], detail=True)
    def remove_genre(self, request, pk):
        """DELETE request to remove genres from a song"""
        song = Song.objects.get(pk=pk)
        genre = Genre.objects.get(id=request.data['genre'])
        song_genre = SongGenre.objects.get(song_id=song, genre_id=genre)
        song_genre.delete()
        return Response({'message': 'Genre removed'}, status=status.HTTP_204_NO_CONTENT)

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genre"""
    class Meta:
        model = SongGenre
        fields = ('genre_id', )
        depth = 1

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""
    genre_count = serializers.IntegerField(default=None)
    genres = SongGenreSerializer(many=True, read_only=True)
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length', 'genre_count', 'genres')
        depth = 1

class AllSongSerializer(serializers.ModelSerializer):
    """JSON serialzer for songs with no genre info"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')