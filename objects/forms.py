from django import forms

from objects.models import Event


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['description', 'lat', 'lon']

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        super(EventForm, self).__init__(*args, **kwargs)

    def save(self, commit=True):
        event = super(EventForm, self).save(commit=False)
        if not event.pk:
            event.user = self.request.user

        if commit:
            event.save()

        return event