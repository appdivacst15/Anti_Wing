from django.shortcuts import render
from django.views.generic import TemplateView


# Create your views here.
class IndexView(TemplateView):
    template_name = "index.html"

    def get(self, request):
        return render(request, self.template_name)


