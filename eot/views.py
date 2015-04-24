import json
from django.http import JsonResponse
from django.views.generic import TemplateView


class JsonView(TemplateView):
    force_ajax = False

    def render(self, data):
        if self.request.is_ajax() or self.force_ajax:
            return JsonResponse(data, safe=False)
        else:
            return super(JsonView, self).render_to_response(data)

    def post_data(self):
        if self.request.is_ajax():
            return json.load(self.request)
        else:
            return self.request.POST
