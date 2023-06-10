from rest_framework import serializers
from tunaapi.models.artist import Artist

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