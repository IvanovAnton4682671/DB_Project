
from django.db import models


class Users(models.Model):
    nickname = models.CharField(max_length=40)
    email = models.CharField(max_length=40)
    password = models.CharField(max_length=56)

    def __str__(self):
        return f"{self.id} {self.nickname} {self.email} {self.password}"

    class Meta:
        db_table = "users"
