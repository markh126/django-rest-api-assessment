from rest_framework import serializers
# from tunaapi.models.songgenre import SongGenre
from tunaapi.models.genre import Genre

# class SongGenreSerializerTwo(serializers.ModelSerializer):
#     """JSON serializer for song genre"""
#     class Meta:
#         model = SongGenre
#         fields = ('song_id', )
#         depth = 1

class GenreSerializer(serializers.ModelSerializer):
    """JSON Serializer for genres"""
    songs = serializers.SerializerMethodField()
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        
    def get_songs(self, obj):
        """Return genre info"""
        songs = obj.songs.all()
        return [{'title': song.song_id.title, 'album': song.song_id.album, 'length': song.song_id.length} for song in songs]

class AllGenreSerializer(serializers.ModelSerializer):
    """JSON Serializer for all genres with no song info"""
    class Meta:
        model = Genre
        fields = ('id', 'description')
