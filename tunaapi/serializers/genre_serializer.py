from rest_framework import serializers
from tunaapi.models.songgenre import SongGenre
from tunaapi.models.genre import Genre

class SongGenreSerializerTwo(serializers.ModelSerializer):
    """JSON serializer for song genre"""
    class Meta:
        model = SongGenre
        fields = ('song_id', )
        depth = 1

class GenreSerializer(serializers.ModelSerializer):
    """JSON Serializer for genres"""
    songs = SongGenreSerializerTwo(many=True, read_only=True)
    class Meta:
        model = Genre
        fields = ('id', 'description', 'songs')
        
class AllGenreSerializer(serializers.ModelSerializer):
    """JSON Serializer for all genres with no song info"""
    class Meta:
        model = Genre
        fields = ('id', 'description')
