import json

from django.views.decorators.csrf import csrf_exempt

from eot.views import JsonView
from users.forms import ProfileForm
from users.models import User


class UserDataMixin:
    def get_user_data(self, user):
        return {
            'name': user.get_full_name(),
            'avatar': user.get_avatar(),
            'rating': user.rating,
        }


class RatingList(UserDataMixin, JsonView):
    def get(self, *args, **kwargs):
        users_qs = User.objects.all().order_by('-rating')
        data = [self.get_user_data(user) for user in users_qs[:20]]
        return self.render(data)

rating = RatingList.as_view()


class ProfileView(UserDataMixin, JsonView):
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated():
            return self.render(self.get_user_data(self.request.user))
        else:
            return self.render({})

    def post(self, *args, **kwargs):
        if not self.request.user.is_authenticated():
            return self.render({'error': 'Please log in before posting'})

        form = ProfileForm(data=json.load(self.request), instance=self.request.user)
        if form.is_valid():
            form.save()
            return self.get(*args, **kwargs)
        else:
            return self.render({'error': 'Data is invalid', 'errors_list': form.errors})

profile = csrf_exempt(ProfileView.as_view())

