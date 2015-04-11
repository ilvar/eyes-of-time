from django.conf.urls import include, url
from django.contrib import admin

urlpatterns = [
    # Examples:
    url(r'^$', 'objects.views.home', name='home'),
    url(r'^events/$', 'objects.views.events', name='events'),

    url(r'^rating/$', 'users.views.rating', name='rating'),
    url(r'^profile/$', 'users.views.profile', name='profile'),

    url(r'^accounts/', include('social.apps.django_app.urls', namespace='social')),

    url(r'^admin/', include(admin.site.urls)),
]
