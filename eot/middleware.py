import re

from django.shortcuts import redirect
from django.http import HttpResponseRedirect
from django.conf import settings

EXEMPT_URLS = [re.compile(settings.LOGIN_URL.lstrip('/')), re.compile('^privacy/')]

if hasattr(settings, 'LOGIN_EXEMPT_URLS'):
    EXEMPT_URLS += [re.compile(expr) for expr in settings.LOGIN_EXEMPT_URLS]


class LoginRequiredMiddleware:
    """
    Middleware that requires a user to be authenticated to view any page other
    than LOGIN_URL. Exemptions to this requirement can optionally be specified
    in settings via a list of regular expressions in LOGIN_EXEMPT_URLS (which
    you can copy from your urls.py).

    Requires authentication middleware and template context processors to be
    loaded. You'll get an error if they aren't.
    """
    def process_request(self, request):
        if not request.user.is_authenticated():
            path = request.path_info.lstrip('/')
            if not any(m.match(path) for m in EXEMPT_URLS):
                return HttpResponseRedirect(settings.LOGIN_URL)


class MobileSSOMiddleware(object):
    def process_request(self, request):
        mobile_redirect = request.GET.get('mobile')
        if mobile_redirect:
            request.session['mobile'] = mobile_redirect
            return redirect('/accounts/login/facebook/?next=/')

        if request.path == '/' or request.path == '/accounts/profile/':
            mobile_url = request.session.get('mobile')
            if mobile_url:
                del request.session['mobile']
                return redirect(mobile_url)
