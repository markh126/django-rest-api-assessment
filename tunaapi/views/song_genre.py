from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.songgenre import SongGenre

class SongGenreView(ViewSet):
    """Tuna API Song Genres"""
    def retrieve(self, request, pk):
        """GET request for a single song genre"""
        try:
            song_genre = SongGenre.objects.get(pk=pk)
            serializer = SongGenreSerializer(song_genre)
            return Response(serializer.data)
        except SongGenre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for a list of song genres"""
        song_genres = SongGenre.objects.all()
        serializer = SongGenreSerializer(song_genres, many=True, context={'request': request})
        return Response(serializer.data)

class SongGenreSerializer(serializers.ModelSerializer):
    """JSON serializer for song genres"""
    class Meta:
        model = SongGenre
        fields = ('id', 'song_id', 'genre_id')
        depth = 1
