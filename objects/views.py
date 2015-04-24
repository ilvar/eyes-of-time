import json
import urllib
import datetime
from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect

from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, DetailView
from django.contrib.humanize.templatetags.humanize import naturaltime
from eot.views import JsonView
from objects.forms import EventForm

from objects.models import Event, Like


class HomeView(TemplateView):
    template_name = 'home.html'

home = HomeView.as_view()


class EventsList(JsonView):
    template_name = 'event.html'

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

        ds = self.kwargs.get('date')
        if ds:
            d = datetime.datetime.strptime(ds, '%d.%m.%Y').date()
            events_qs = events_qs.filter(added__day=d.day, added__month=d.month, added__year=d.year)

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

    def get_context_data(self, **kwargs):
        data = super(EventsDetail, self).get_context_data(**kwargs)
        if self.request.user.is_authenticated():
            data['like'] = Like.objects.filter(event=self.get_object(), user=self.request.user).first()
        return data

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            messages.error(self.request, 'You should be <a href="/login/">authenticated</a>')
            return redirect('.')

        Like.objects.get_or_create(event=self.get_object(), user=self.request.user)
        messages.success(self.request, 'You like this event!')
        return redirect('.')

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
