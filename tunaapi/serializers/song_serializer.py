from rest_framework import serializers
# from tunaapi.models.songgenre import SongGenre
from tunaapi.models.song import Song

# class SongGenreSerializerOne(serializers.ModelSerializer):
#     """JSON serializer for song genre"""
#     class Meta:
#         model = SongGenre
#         fields = ('genre_id', )
#         depth = 1

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for songs"""
    genre_count = serializers.IntegerField(default=None)
    genres = serializers.SerializerMethodField()
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length', 'genre_count', 'genres')

    def get_genres(self, obj):
        """Return genre info"""
        genres = obj.genres.all()
        return [{'description': genre.genre_id.description} for genre in genres]

class AllSongSerializer(serializers.ModelSerializer):
    """JSON serialzer for songs with no genre info"""
    class Meta:
        model = Song
        fields = ('id', 'title', 'artist_id', 'album', 'length')