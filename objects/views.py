import json
import urllib
from django.http import HttpResponse

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView
from django.contrib.humanize.templatetags.humanize import naturaltime
from eot.views import JsonView
from objects.forms import EventForm

from objects.models import Event


class HomeView(TemplateView):
    template_name = 'home.html'

home = HomeView.as_view()


class EventsList(JsonView):
    def get_event_data(self, event):
        return {
            'pk': event.pk,
            'url': event.get_absolute_url(),
            'user': unicode(event.user.get_full_name()),
            'img': event.img and event.img.url or '',
            'avatar': event.user.get_avatar(),
            'description': event.description,
            'coordinates': map(float, [event.lat, event.lon]),
            'added': naturaltime(event.added)
        }

    def get(self, *args, **kwargs):
        events_qs = Event.objects.all().select_related('user').order_by('-added')
        data = [self.get_event_data(event) for event in events_qs[:100]]
        return self.render(data)

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.render({'error': 'Please log in before posting'})

        form = EventForm(data=json.load(self.request), request=self.request)
        if form.is_valid():
            event = form.save()
            return self.render(self.get_event_data(event))
        else:
            return self.render({'error': 'Data is invalid', 'errors_list': form.errors})

events = csrf_exempt(EventsList.as_view())


class EventsDetail(DetailView):
    model = Event
    template_name = 'event.html'

one_event = EventsDetail.as_view()


class PrivacyView(TemplateView):
    template_name = 'privacy.html'

privacy = PrivacyView.as_view()


class TileProxyView(View):
    def get(self, *args, **kwargs):
        url = 'https://map1.vis.earthdata.nasa.gov/wmts-webmerc/MODIS_Terra_CorrectedReflectance_TrueColor/default/'
        url += self.request.path[6:]
        return HttpResponse(urllib.urlopen(url), content_type='image/jpeg')

tile_proxy = TileProxyView.as_view()
