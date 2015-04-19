import base64
import random
import re
import string

from django import forms
from django.core.files.base import ContentFile

from objects.models import Event


class EventForm(forms.ModelForm):
    dataURL = forms.CharField()

    class Meta:
        model = Event
        fields = ['description', 'lat', 'lon', 'date']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(EventForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)
        if not event.pk:
            event.user = self.request.user

        data_url = self.cleaned_data.get('dataURL')
        if data_url:
            img_prefix = 'data:image/png;base64,'
            assert data_url.startswith(img_prefix)

            data_url = data_url[len(img_prefix):]
            img_data = base64.b64decode(data_url)

            random_name = ''.join(random.sample(string.digits + string.letters, 16)) + '.png'

            event.img.save(random_name, ContentFile(img_data), save=commit)
        else:
            if commit:
                event.save()

        if '#' in event.description:
            tags = re.findall('\#\w+', event.description)
            tags = [t.strip('#') for t in tags]
            event.tags.set(*tags)

        return event
