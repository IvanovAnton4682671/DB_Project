
from django.db import models


class Users(models.Model):
    nickname = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=56)

    def __str__(self):
        return f"{self.id} {self.nickname} {self.email} {self.password}"

    class Meta:
        db_table = "users"

class MusicBase(models.Model):
    genre = models.CharField(max_length=30)
    author = models.CharField(max_length=40)
    co_author = models.CharField(max_length=40)
    album = models.CharField(max_length=30)
    title = models.CharField(max_length=40)

    def __str__(self):
        return f"{self.id} {self.genre} {self.author} {self.co_author} {self.album} {self.title}"

    class Meta:
        db_table = "music_base"
