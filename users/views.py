import json
from django.contrib import messages

from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.contrib.auth import logout as auth_logout

from eot.views import JsonView
from users.forms import ProfileForm
from users.models import User


class UserDataMixin:
    def get_user_data(self, user):
        return {
            'pk': user.pk,
            'name': user.get_full_name(),
            'avatar': user.get_avatar(),
            'rating': user.rating,
        }


class LoginView(TemplateView):
    """
    View for authenticating users
    """
    template_name = 'login.html'

login = LoginView.as_view()


def logout(request):
    """
    logout user
    :return:
    """
    auth_logout(request)
    return redirect(reverse('login'))


class RatingList(UserDataMixin, JsonView):
    template_name = 'rating.html'

    def get(self, *args, **kwargs):
        users_qs = User.objects.all().order_by('-rating')
        data = [self.get_user_data(user) for user in users_qs[:20]]
        if self.request.is_ajax():
            return self.render(data)
        else:
            return self.render({'rating': data})

rating = RatingList.as_view()


class ProfileView(UserDataMixin, JsonView):
    template_name = 'profile.html'

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return self.render(self.get_user_data(self.request.user))
        else:
            return self.render({})

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.render({'error': 'Please log in before posting'})

        form = ProfileForm(data=self.post_data(), instance=self.request.user)
        if form.is_valid():
            form.save()
            if not self.request.is_ajax():
                messages.success(self.request, u'Data saved.')
                return redirect('.')
            else:
                return self.get(*args, **kwargs)
        else:
            return self.render({'error': 'Data is invalid', 'errors_list': form.errors})

profile = csrf_exempt(ProfileView.as_view())

