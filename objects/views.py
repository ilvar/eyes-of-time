import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View
from objects.forms import EventForm

from objects.models import Event


class HomeView(TemplateView):
    template_name = 'home.html'

home = HomeView.as_view()


class JsonView(View):
    @staticmethod
    def render(data):
        return JsonResponse(data, safe=False)


class EventsList(JsonView):
    def get(self, *args, **kwargs):
        events_qs = Event.objects.all().select_related('user')
        data = [{
            'user': unicode(event.user),
            'description': event.description,
            'coordinates': map(float, [event.lat, event.lon])
        } for event in events_qs[:100]]
        return self.render(data)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.render({'error': 'Please log in before posting'})

        form = EventForm(data=json.load(self.request), request=self.request)
        if form.is_valid():
            form.save()
            return self.get(*args, **kwargs)
        else:
            return self.render({'error': 'Data is invalid', 'errors_list': form.errors})

events = csrf_exempt(EventsList.as_view())