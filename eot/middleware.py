from django.shortcuts import redirect


class MobileSSOMiddleware(object):
    def process_request(self, request):
        if request.GET.get('next'):
            request.session['mobile'] = request.GET.get('next')
            return redirect('/accounts/login/facebook/?next=/')

        if request.path == '/' or request.path == '/accounts/profile/':
            mobile_url = request.session.get('mobile')
            if mobile_url:
                del request.session['mobile']
                return redirect(mobile_url)