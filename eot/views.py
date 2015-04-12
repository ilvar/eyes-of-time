from django.http import JsonResponse
from django.views.generic import View


class JsonView(View):
    @staticmethod
    def render(data):
        return JsonResponse(data, safe=False)


