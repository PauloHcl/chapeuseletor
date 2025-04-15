from django.db import models

class Participant(models.Model):
    nick = models.CharField(max_length=100, unique=True)
    answers = models.JSONField()
    final_house = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.nick} - {self.final_house}"
