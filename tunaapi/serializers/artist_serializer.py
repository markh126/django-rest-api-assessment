from rest_framework import serializers
from tunaapi.models.artist import Artist
from tunaapi.models.song import Song

class SongSerializer(serializers.ModelSerializer):
    """JSON serializer for song genre"""
    class Meta:
        model = Song
        fields = ('title', 'album', 'length')

class ArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists"""
    song_count = serializers.IntegerField(default=None)
    songs = SongSerializer(many=True)
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio', 'song_count', 'songs')
        depth = 1

class AllArtistSerializer(serializers.ModelSerializer):
    """JSON serializer for artists with no song info"""
    class Meta:
        model = Artist
        fields = ('id', 'name', 'age', 'bio')