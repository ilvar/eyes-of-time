import json
from django.http import HttpResponse

from django.views.generic import TemplateView, View
from objects.forms import EventForm

from objects.models import Event


class HomeView(TemplateView):
    template_name = 'home.html'

home = HomeView.as_view()


class JsonView(View):
    @staticmethod
    def render(data):
        return HttpResponse(json.dumps(data), content_type='application/json')


class EventsList(JsonView):
    def get(self, *args, **kwargs):
        events_qs = Event.objects.all().select_related('user')
        data = [{
            'user': unicode(event.user),
            'description': event.description,
            'coordinates': [event.lat, event.lon]
        } for event in events_qs[:100]]
        return self.render(data)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.render({'error': 'Please log in before posting'})

        form = EventForm(data=self.request.POST, request=self.request)
        if form.is_valid():
            form.save()
            return self.get(*args, **kwargs)
        else:
            return self.render({'error': 'Data is invalid', 'errors_list': form.errors})

events = EventsList.as_view()