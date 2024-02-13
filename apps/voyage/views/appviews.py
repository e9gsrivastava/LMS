from django.views.generic import TemplateView

from qux.seo.mixin import SEOMixin


class VoyageDefaultView(SEOMixin, TemplateView):
    template_name = "voyage/index.html"

