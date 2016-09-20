from django.views.generic import TemplateView


class SimpleDemoView(TemplateView):
    template_name = 'reactjs_demo/simple.django.html'
