from django.db import models


class Event(models.Model):
    user = models.ForeignKey('users.User')
    description = models.CharField(max_length=140)

    # Ratings
    likes = models.PositiveIntegerField(default=0, editable=0)

    added = models.DateTimeField(auto_now_add=True)


class Like(models.Model):
    user = models.ForeignKey('users.User')
    event = models.ForeignKey(Event)
    added = models.DateTimeField(auto_now_add=True)
