import hashlib

from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    name = models.CharField(max_length=255, null=True)

    # Ratings
    time_spent = models.PositiveIntegerField(default=0, editable=0)
    findings_count = models.PositiveIntegerField(default=0, editable=0)
    rating = models.PositiveIntegerField(default=0, editable=0)

    def get_full_name(self, *args, **kwargs):
        return self.name or 'User %s' % self.pk

    def get_avatar(self):
        fb = self.social_auth.filter(provider='facebook').first()
        if fb:
            return 'https://graph.facebook.com/%s/picture?type=square' % fb.uid

        return 'http://www.gravatar.com/avatar/%s?s=50' % hashlib.md5(self.email).hexdigest()
