"""View module for handling requests about genres"""
from django.http import HttpResponseServerError
from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework import serializers, status
from tunaapi.models.genre import Genre

class GenreView(ViewSet):
    """Tuna API genres"""
    def retrieve(self, request, pk):
        """GET request for a single genre object"""
        try:
            genre = Genre.objects.get(pk=pk)
            serializer = GenreSerializer(genre)
            return Response(serializer.data)
        except Genre.DoesNotExist as ex:
            return Response({'message': ex.args[0]}, status=status.HTTP_404_NOT_FOUND)

    def list(self, request):
        """GET request for a list of genre objects"""
        genres = Genre.objects.all()
        serializer = GenreSerializer(genres, many=True, context={'request': request})
        return Response(serializer.data)

    def create(self, request):
        """POST request to create a genre object"""
        genre = Genre.objects.create(
            description=request.data["description"]
        )
        serializer = GenreSerializer(genre)
        return Response(serializer.data)

    def update(self, request, pk):
        """PUT request to update a genre object"""
        genre = Genre.objects.get(pk=pk)
        genre.description = request.data['description']
        genre.save()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

    def destroy(self, request, pk):
        """DELETE request to destroy a genre object"""
        genre = Genre.objects.get(pk=pk)
        genre.delete()
        return Response({}, status=status.HTTP_204_NO_CONTENT)

class GenreSerializer(serializers.ModelSerializer):
    """JSON Serializer for genres"""
    class Meta:
        model = Genre
        fields = ('id', 'description')
