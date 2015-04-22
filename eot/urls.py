from django.conf import settings
from django.conf.urls import include, url
from django.conf.urls.static import static
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'objects.views.home', name='home'),
    url(r'^events/$', 'objects.views.events', name='events'),
    url(r'^events/(?P<date>\d{2}\.\d{2}.\d{4})/$', 'objects.views.events', name='events'),
    url(r'^events/(?P<pk>\d+)/$', 'objects.views.one_event', name='one_event'),

    url(r'^privacy/$', 'objects.views.privacy', name='privacy'),
    url(r'^tile/(.*)$', 'objects.views.tile_proxy', name='tile'),

    url(r'^login/$', 'users.views.login', name='login'),
    url(r'^exit/$', 'users.views.logout', name='logout'),
    url(r'^rating/$', 'users.views.rating', name='rating'),
    url(r'^profile/$', 'users.views.profile', name='profile'),

    url(r'^accounts/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^admin/', include(admin.site.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
