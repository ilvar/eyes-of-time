from django.shortcuts import redirect


class MobileSSOMiddleware(object):
    def process_request(self, request):
        if request.GET.get('next'):
            request.session['mobile'] = request.GET.get('next')

        if request.GET.get('logged'):
            mobile_url = request.session.get('mobile')
            if mobile_url:
                del request.session['mobile']
                return redirect(mobile_url)