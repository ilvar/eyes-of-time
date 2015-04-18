from django.core.urlresolvers import reverse
from django.db import models

from taggit.managers import TaggableManager


class Event(models.Model):
    user = models.ForeignKey('users.User')
    description = models.CharField(max_length=140)
    lat = models.DecimalField(max_digits=20, decimal_places=16)
    lon = models.DecimalField(max_digits=20, decimal_places=16)
    img = models.ImageField(null=True, editable=False)

    # Ratings
    likes = models.PositiveIntegerField(default=0, editable=0)
    tags = TaggableManager()

    added = models.DateTimeField(auto_now_add=True)

    def get_absolute_url(self):
        return reverse('one_event', args=[self.pk])


class Like(models.Model):
    user = models.ForeignKey('users.User')
    event = models.ForeignKey(Event)
    added = models.DateTimeField(auto_now_add=True)


def recount_findings(instance, created, *args, **kwargs):
    if not created:
        return

    instance.user.findings_count = Event.objects.filter(user=instance.user).count()
    instance.user.rating = Event.objects.filter(user=instance.user).count()  # TODO: better calc
    instance.user.save()

models.signals.post_save.connect(recount_findings, sender=Event)
