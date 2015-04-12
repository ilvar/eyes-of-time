from django.views.generic import TemplateView


class LoginView(TemplateView):
    """
    View for authenticating users
    """
    template_name = 'login.html'

login = LoginView.as_view()
