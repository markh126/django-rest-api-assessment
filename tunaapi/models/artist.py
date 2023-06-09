from django.db import models

class Artist(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField()
    bio = models.CharField(max_length=200)

    @property
    def songs(self):
        """Event specific info"""
        info = []
        for song in self.artist_songs.all():
            info.append(song.title)
        return info
